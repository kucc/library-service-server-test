from dotenv import load_dotenv, dotenv_values
import os

load_dotenv() # take environment variables from .env.

print(os.getenv(("DB_DB")))