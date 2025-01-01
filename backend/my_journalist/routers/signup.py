import logging

import uuid
from fastapi import APIRouter, Request, HTTPException, status
import bcrypt

from my_journalist.utils.logger import setup_logging
from my_journalist.database.models import User
from my_journalist.database.schemas import UserInput
from my_journalist.database.crud import add_user

setup_logging()

logger = logging.getLogger(__name__)

signup_router = APIRouter()

@signup_router.post("/signup")
async def signup(payload:UserInput):
    try:
        id = str(uuid.uuid4())
        password = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode() #convert type from bytes to string
        user = User(id=id, name=payload.name, email=payload.email, password=password)
        result = await add_user(user)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email已存在")
        return {"message": "帳號成功建立！請重新登入"}
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to signup") from e