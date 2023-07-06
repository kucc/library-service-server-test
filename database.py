from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

db_host = settings.DB_HOST
db_port = settings.DB_PORT
db_user = settings.DB_USER
db_password = settings.DB_PASSWORD
db_db = settings.DB_DB

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://" + db_user + ":" + db_password + "@" + db_host + ":" + str(db_port) + "/" + db_db

class Engineconn:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=500)
    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()
        return conn