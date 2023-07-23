from dotenv import load_dotenv, dotenv_values
import os

load_dotenv() # take environment variables from .env.

# database
DB_DB = os.getenv("DB_DB")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")

db_port = os.getenv("DB_PORT") # 테스트용
if db_port is not None and db_port.isdigit():
    print("DB_PORT is digit. DB_PORT is set to ")
    print("DB_PORT is digit. DB_PORT is set to ")
    print("DB_PORT is digit. DB_PORT is set to ")
    print("DB_PORT is digit. DB_PORT is set to ")
    print("DB_PORT is digit. DB_PORT is set to ")
    db_port = int(os.getenv("DB_PORT"))
    print(type(db_port))
    print(type(db_port))
    print(type(db_port))
    print(type(db_port))
    print(type(db_port))
else:
    print("DB_PORT is not digit. DB_PORT is set to 3306", type(db_port))
    print("DB_PORT is not digit. DB_PORT is set to 3306", type(db_port))
    print("DB_PORT is not digit. DB_PORT is set to 3306", type(db_port))
    print("DB_PORT is not digit. DB_PORT is set to 3306", type(db_port))
    print("DB_PORT is not digit. DB_PORT is set to 3306", type(db_port))

DB_USER = os.getenv("DB_USER")

# firebase authentication & authorization
FB_SALT_SEPARATOR = os.getenv("FB_SALT_SEPARATOR")
FB_SIGNER_KEY = os.getenv("FB_SIGNER_KEY")
FB_ROUNDS = os.getenv("FB_ROUNDS")
FB_MEM_COST = os.getenv("FB_MEM_COST")

from pydantic import BaseSettings

class Settings(BaseSettings):
    db_db: str = DB_DB
    db_host: str = DB_HOST
    db_password: str = DB_PASSWORD
    db_port: int = db_port
    db_user: str = DB_USER

    fb_salt_separator: str = FB_SALT_SEPARATOR
    fb_signer_key: str = FB_SIGNER_KEY
    fb_rounds: int = FB_ROUNDS
    fb_mem_cost: int = FB_MEM_COST

# https://medium.com/@mohit_kmr/production-ready-fastapi-application-from-0-to-1-part-3-a1ff8c700d9c
# https://www.linkedin.com/pulse/dotenv-files-app-security-fastapi-prince-odoi/