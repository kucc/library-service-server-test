from app.internal.custom_exception import *
from app.internal.schemas.schema import *
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.inspection import inspect
from datetime import datetime, time
from typing import Dict, Any

# TODO :
#  user_mode, use_updated_at를 쿼리 파라미터 제외
#  use_updated_at : back단에서 설정하고 client가 설정하지 않도록 함
#  user_mode : user가 사용하는 api에서는 쿼리 파라미터 제외, admin이 사용하는 api는 쿼리 파라미터로 설정, default true

def filter_by_period(*,
                     query,
                     model,
                     p,
                     use_updated_at: bool | None = False):
    '''
    조회 기간을 기준으로 한 filtering
    :param query: database session의 query
    :param model: filtering이 이뤄질 database의 table
    :param p: object, get_begin(조회 시작 날짜), get_end(조회 종료 날짜)가 포함됨
    :param use_updated_at: 기간 조회에 사용될 model의 column 설정
                           True - update_at(수정일), False : create_at(등록일)
                           default : False
    :return: query
    '''
    date_column = model.updated_at if use_updated_at else model.created_at
    for attr, value in p.__dict__.items():
        if value:
            if attr == 'get_begin':
                parsed_date = datetime.combine(value, time.min)
                query = query.filter(date_column >= parsed_date)
            elif attr == 'get_end':
                parsed_date = datetime.combine(value, time.max)
                query = query.filter(date_column <= parsed_date)
    return query


# FILTERING LOGIC CODE 간소화 함수
def filters_by_query(query, model, q):
    for attr, value in q.__dict__.items():
        if value:
            if isinstance(value, str):
                query = query.filter(getattr(model, attr).ilike(f"%{value}%"))
            elif isinstance(value, (int, bool)):
                if attr != 'rating':
                    query = query.filter(getattr(model, attr) == value)
                else:
                    filter_expression = and_(value + 1 > getattr(model, attr), getattr(model, attr) >= value)
                    query = query.filter(filter_expression)
    return query


# order_by 간소화 함수
def orders_by_query(query, model, o):
    for attr, value in o.__dict__.items():
        try:
            if value is None:
                continue
            if value is False:
                query = query.order_by(getattr(model, attr).asc())
            if value is True:
                query = query.order_by(getattr(model, attr).desc())
        except AttributeError:
            continue
    return query

# 명시적 외래키 값 존재 확인
# 성능 최적화 또는 자세한 오류 처리와 같이 데이터를 삽입하기 전에 외래 키 값의 존재를 확인해야 하는 특정 요구 사항이 있는 경우
def get_referenced_table_and_fk(model):
    referenced_tables = {}
    for column in model.__table__.columns:
        if column.foreign_keys:
            for fk in column.foreign_keys:
                referenced_tables[column.name] = fk.column.table.name
    return referenced_tables


def valid_referenced_key(model, item, db):
    referenced_tables = get_referenced_table_and_fk(model)
    for attr, value in referenced_tables.items():
        if hasattr(item, attr):
            try:
                refer = get_item_by_column(model=model, columns={attr: getattr(item, attr)}, mode=True, db=db)
            except NoResultFound:
                raise ForeignKeyValidationError((attr, item[attr]))
            else:
                if not refer:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return True

# TODO : ADMIN GET BOOK-INFO에 대한 함수 정의

# get the item by primary key
def get_item_by_id(*,
                   model,
                   index: int,
                   db,
                   user_mode: bool | None = True):
    pk = inspect(model).primary_key[0].name
    try:
        if user_mode:
            item = db.query(model).filter_by(**{pk: index, 'valid': user_mode}).one()
        else:
            item = db.query(model).filter_by(**{pk: index}).one()
    except NoResultFound:
        raise ItemKeyValidationError(detail=(f"{pk}", index))
    finally:
        db.close()
    return item

# get_item_by_column
# column 이름과 value 값을 이용하여 filtering
def get_item_by_column(*,
                       model,
                       columns: Dict[str, Any],
                       mode: bool,
                       db):
    for column_name, value in columns.items() :
        if value:
            if column_name in model.__table__.columns:
                query = db.query(model).filter(getattr(model, column_name) == value)
                query = query.filter(model.valid)
    if mode:
        result = query.all()
        return result
    return query



# CREATE
def create_item(model, req, db):
    item = model(**req.dict())
    try:
        if valid_referenced_key(model, item, db):
            db.add(item)
            db.commit()
            db.refresh(item)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Fail to create the new {model} item. {str(e.orig)}")
    finally:
        db.close()
    return item

# GET
def get_list_of_item(*,
                     model,
                     skip: int,
                     limit: int,
                     use_update_at: bool | None = False,
                     user_mode: bool | None = True,
                     q,
                     p,
                     o,
                     init_query: Any | None = None,
                     db,
                     ):
    if init_query is None:
        init_query = db.query(model)
    query = filters_by_query(init_query, model, q)
    query = filter_by_period(query=query, model=model, p=p, use_updated_at=use_update_at)
    if user_mode:
        query = query.filter(model.valid)
    query = orders_by_query(query, model, o)
    result = query.offset(skip).limit(limit).all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    db.close()

    return result


# update
def update_item(*,
                model,
                req,
                index,
                db):
    item = get_item_by_id(model=model, index=index, db=db, user_mode=True)
    dict_item = item.__dict__
    dict_req = req.__dict__
    try:
        for key in dict_req.keys():
            if key in dict_item:
                if isinstance(dict_req[key], type(dict_item[key])):
                    if valid_referenced_key(model, dict_req, db):
                        setattr(item, key, dict_req[key])
                else:
                    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                        detail=f"Invalid value type for column '{key}'.")
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during update: {str(e)}")
    finally:
        db.close()
    return item


# delete
def delete_item(model, index, db):
    item = get_item_by_id(model=model, index=index, db=db)
    try:
        setattr(item, 'valid', False)
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Unexpected error occurred during delete: {str(e)}")
    finally:
        db.close()
