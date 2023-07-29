from fastapi import HTTPException, status
from datetime import datetime, timedelta, time
import re

# get_begin, get_end 입력값 형식 validation
def check_date_format(date_str):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(pattern, date_str):
        return True
    else:
        return False

# get_begin, get_end query를 이용한 filtering
# TODO : NONE -> DEFAULT 값을 할당하는 로직은 수행하지 않음
def filter_by_period(query, model, q):
    for attr, value in q.__dict__.items():
        if value is not None:
            if check_date_format(value):
                parsed_date = datetime.strptime(value, "%Y-%m-%d")
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Invalid format. It should be in YY-MM-DD format.")
            if attr == 'get_begin':
                parsed_date = datetime.combine(parsed_date, time.min)
                query = query.filter(parsed_date <= model.updated_at)
            elif attr == 'get_end':
                parsed_date = datetime.combine(parsed_date, time.max)
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

