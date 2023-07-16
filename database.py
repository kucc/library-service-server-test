from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Settings

settings = Settings()

db_host = settings.DB_HOST
db_port = settings.DB_PORT
db_user = settings.DB_USER
db_password = settings.DB_PASSWORD
db_db = settings.DB_DB

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}"

class Engineconn:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=500)
    def sessionmaker(self):
        sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=self.engine)
        return sessionLocal

    def connection(self):
        conn = self.engine.connect()
        return conn

