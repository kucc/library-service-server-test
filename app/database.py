from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_Settings


Base = declarative_base()
settings = DB_Settings()

db_host = settings.db_host
db_port = settings.db_port
db_user = settings.db_user
db_password = settings.db_password
db_db = settings.db_db

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}"

class EngineConn:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=500)
    def get_session(self):
        session_local = sessionmaker(autoflush=False, autocommit=False, bind=self.engine)
        return session_local()

    def get_connection(self):
        return self.engine.connect()

def get_db():
    engine_conn = EngineConn()
    try:
        session = engine_conn.get_session()
        yield session
    finally:
        session.close()