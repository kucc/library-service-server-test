from fastapi import HTTPException, status
from datetime import datetime, time
from internal.key_validation import *
from internal.schema import *
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect

def filter_by_period(query, model, p, use_updated_at: bool):
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
                query = query.filter(getattr(model, attr) == value)
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
                column_value = getattr(item, attr)
                query = text(f"SELECT * FROM {value} WHERE {attr} = :column_value")
                refer = db.execute(query, {"column_value": column_value}).fetchone()
            except NoResultFound:
                raise ForeignKeyValidationError((attr, column_value))
            else:
                if not refer:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return True

# TODO : ADMIN은 VALID 상관 없이 GET - 현재 VALID TRUE만 GET
# TODO : ADMIN GET BOOK-INFO에 대한 함수 정의

# get the item by id
def get_item_by_id(model, index, db):
    pk = inspect(model).primary_key[0].name
    try:
        item = db.query(model).filter_by(**{pk: index, 'valid': True}).one()
    except NoResultFound:
        raise ItemKeyValidationError(detail=(f"{pk}", index))
    finally:
        db.close()
    return item


# get list of item
def get_list_of_item(model, skip, limit, use_update_at, q, p, db):
    query = db.query(model)
    query = filters_by_query(query, model, q)
    query = filter_by_period(query, model, p, use_update_at)
    query = query.filter(model.valid)
    result = query.offset(skip).limit(limit).all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return result


# create
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


# update
def update_item(model, req, index, db):
    item = get_item_by_id(model, index, db)
    dict_item = item.__dict__
    dict_req = req.__dict__
    try:
        for key in dict_req.keys():
            if key in dict_item:
                if isinstance(dict_req[key], type(dict_item[key])):
                    if valid_referenced_key(model, req, db):
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
    item= get_item_by_id(model, index, db)
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
