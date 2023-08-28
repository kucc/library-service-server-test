from dotenv import load_dotenv
import os
from pydantic_settings  import BaseSettings

load_dotenv() # take environment variables from .env.

# database
class DB_Settings(BaseSettings):
    db_db: str = os.getenv("DB_DB")
    db_host: str = os.getenv("DB_HOST")
    db_password: str = os.getenv("DB_PASSWORD")
    db_port: int = int(os.getenv("DB_PORT"))
    db_user: str = os.getenv("DB_USER")

# access token
class ACCESS_TOKEN_Settings(BaseSettings):
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM")

# firebase authentication & authorization
class FB_Settings(BaseSettings):
    fb_salt_separator: str = os.getenv("FB_SALT_SEPARATOR")
    fb_signer_key: str = os.getenv("FB_SIGNER_KEY")
    fb_rounds: int = int(os.getenv("FB_ROUNDS"))
    fb_mem_cost: int = int(os.getenv("FB_MEM_COST"))

# https://medium.com/@mohit_kmr/production-ready-fastapi-application-from-0-to-1-part-3-a1ff8c700d9c
# https://www.linkedin.com/pulse/dotenv-files-app-security-fastapi-prince-odoi/