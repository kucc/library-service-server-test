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

