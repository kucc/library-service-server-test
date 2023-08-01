from fastapi import HTTPException, status
from datetime import datetime, time

# get_begin, get_end query를 이용한 filtering
def filter_by_period(query, model, p):
    for attr, value in p.__dict__.items():
        if value:
            if attr == 'get_begin':
                parsed_date = datetime.combine(value, time.min)
                query = query.filter(parsed_date <= model.updated_at)
            elif attr == 'get_end':
                parsed_date = datetime.combine(value, time.max)
                query = query.filter(parsed_date >= model.updated_at)
    return query


# FILTERING LOGIC CODE 간소화 함수
def filters_by_query(query, model, q):
    for attr, value in q.__dict__.items():
        if value is not None:
            if isinstance(value, str):
                query = query.filter(getattr(model, attr).ilike(f"%{value}%"))
            elif isinstance(value, (int, bool)):
                query = query.filter(getattr(model, attr) == value)
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
    '''
    if o.by_rating is False:
        query = query.order_by(model.rating.asc())
    if o.by_rating is True:
        query = query.order_by(model.rating.desc())
    if o.by_publication_year is False:
        query = query.order_by(model.publication_year.asc())
    if o.by_publication_year is True:
        query = query.order_by(model.publication_year.desc())
    if o.by_the_newest is False:
        query = query.order_by(model.created_at.asc())
    if o.by_the_newest is True:
        query = query.order_by(model.created_at.desc())    
    if o.by_title is False:
        query = query.order_by(model.title.asc())
    if o.by_title is True:
        query = query.order_by(model.title.desc())
    '''