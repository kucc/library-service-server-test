from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import Settings


Base = declarative_base()
settings = Settings()

db_host = settings.DB_HOST
db_port = settings.DB_PORT
db_user = settings.DB_USER
db_password = settings.DB_PASSWORD
db_db = settings.DB_DB

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