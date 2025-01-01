import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER=os.environ.get("DATABASE_USER")
DATABASE_PASSWORD=os.environ.get("DATABASE_PASSWORD")
DATABASE_HOST=os.environ.get("DATABASE_HOST")
DATABASE_PORT=os.environ.get("DATABASE_PORT")
DATABASE_DB=os.environ.get("DATABASE_DB")

url = f"postgresql+psycopg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"

# Redis conncection string
REDIS_HOST=os.environ.get("REDIS_HOST")
REDIS_PORT=os.environ.get("REDIS_PORT")
REDIS_DB=os.environ.get("REDIS_DB")

class Settings:
    DATABASE_URL: str = url
    REDIS_HOST : str = REDIS_HOST
    REDIS_PORT : str = REDIS_PORT
    REDIS_DB : int = REDIS_DB

settings = Settings()