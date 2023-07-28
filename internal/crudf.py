# FILTERING LOGIC CODE 간소화 함수
def filters_by_q(query, model, q):
    for attr, value in q.__dict__.items():
        if value is not None:
            if isinstance(value, str):
                query = query.filter(getattr(model, attr).ilike(f"%{value}%"))
            elif isinstance(value, (int, bool)):
                query = query.filter(getattr(model, attr) == value)
    return query