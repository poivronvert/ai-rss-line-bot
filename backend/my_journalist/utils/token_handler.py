import os
import logging
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

import jwt

load_dotenv()

USER_INFO_TOKEN_SECRET = os.getenv("USER_INFO_TOKEN_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    logging.info(to_encode)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    logging.info(to_encode)
    encoded_jwt = jwt.encode(to_encode, USER_INFO_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    return jwt.decode(token, USER_INFO_TOKEN_SECRET, algorithms=ALGORITHM)

