import logging
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status

from my_journalist.utils.logger import setup_logging
from my_journalist.database.schemas import UserSignin, Token
from my_journalist.database.crud import check_user_logged_in
from my_journalist.utils.token_handler import create_token

setup_logging()

logger = logging.getLogger(__name__)

signin_router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@signin_router.post("/signin")
async def signin(payload: UserSignin):
    try:
        result = await check_user_logged_in(payload)
        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="帳號或密碼錯誤")
        token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_token(result, token_expires)
        return Token(token=token, token_type="bearer")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Failed to signin: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to signin")
