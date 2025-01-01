import os
import sys
import logging
import requests
import uuid
import secrets
import json
from  datetime import datetime, timedelta, timezone

from fastapi import Request, APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from redis import RedisError
from dotenv import load_dotenv

from my_journalist.database.crud import get_today_article, add_user
from my_journalist.database.schemas import BroadcastPayload, Token, LineUser
from my_journalist.database.models import User
from my_journalist.database.db import redis_client
from my_journalist.utils.logger import setup_logging
from my_journalist.utils.token_handler import create_token

setup_logging()

logger = logging.getLogger(__name__)

load_dotenv()

channel_access_token = os.getenv("LINE_MESSAGING_CHANNEL_ACCESS_TOKEN", None)
API_TOKEN = os.getenv("API_TOKEN")
LINE_LOGIN_CHANNEL_ID = os.getenv("LINE_LOGIN_CHANNEL_ID")
LINE_LOGIN_CHANNEL_SECRET = os.getenv("LINE_LOGIN_CHANNEL_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

linebot_router = APIRouter()

def broadcast_message(channel_access_token:str, messages:list):
    broadcast_url="https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type":"application/json",
        "Authorization":f"Bearer {channel_access_token}",
        "X-Line-Retry-Key":str(uuid.uuid4())
    }
    payload = {
        "messages":messages
    }

    try:
        broadcast_response = requests.post(broadcast_url, headers=headers, json=payload)
        broadcast_response.raise_for_status()
        return broadcast_response.json()
    
    except requests.exceptions.RequestException as e:
        if e.response:
            status_code = e.response.status_code
            detail = e.response.json()
            logger.error(f"Error in broadcast message: {detail}")
            raise HTTPException(status_code=status_code, detail=detail)
    
    except Exception as e:
        logger.error(f"Unexpected error in broadcast_message: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@linebot_router.post("/broadcast")
async def send_broadcast(payload: BroadcastPayload):

    token = payload.token
    
    if token != API_TOKEN:
        logger.error(f"Invalid token: {token}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail="Unauthorized token")
    
    url=f'{os.getenv("FRONTEND_URL")}/posts/'

    today_article = await get_today_article()

    if not today_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No article found")
    
    if len(today_article) > 2:
        texts = f"{today_article[1]} \n\n {today_article[2]} \n\n {url}{today_article[0]}"
    else:
        texts = today_article[1]

    messages = [
        {
            "type":"text",
            "text":texts
        }
    ]
    try:
        result = broadcast_message(channel_access_token, messages)
        return result
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        logger.error(f"Failed to send broadcast: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send broadcast message")

async def get_line_login_token(code: str):
    try:
        token_url = "https://api.line.me/oauth2/v2.1/token"
        r_uri = os.environ.get("LINE_LOGIN_URI")
        client_id = LINE_LOGIN_CHANNEL_ID
        client_secret = LINE_LOGIN_CHANNEL_SECRET

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": r_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        token_response = requests.post(token_url, headers=headers, data=data)
        logger.info(f"Token response: {token_response.json()}")
        
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get("access_token")


        return access_token

    except requests.exceptions.RequestException as e:
        if e.response:
            status_code = e.response.status_code
            detail = e.response.json()
            logger.error(f"Error in line login token: {detail}")
            raise HTTPException(status_code=status_code, detail=detail)
    
    except Exception as e:
        logger.error(f"Unexpected error in line login receive: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

async def line_login_verify(access_token: str):
    verify_url = "https://api.line.me/oauth2/v2.1/verify"
    params = {
        "access_token": access_token
    }

    try: 
        verify_response = requests.get(verify_url, params=params)
        verify_response.raise_for_status()
        return verify_response.json()
    
    except requests.exceptions.RequestException as e:
        if e.response:
            status_code = e.response.status_code
            detail = e.response.json()
            logger.error(f"Error in line login verify: {detail}")
            raise HTTPException(status_code=status_code, detail=detail)
        
    except Exception as e:
        logger.error(f"Unexpected error in line login verify: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

async def line_login_profile(access_token: str):
    try:
        profile_url = "https://api.line.me/v2/profile"
        headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = requests.get(profile_url, headers=headers)
        profile_response.raise_for_status()

        return profile_response.json()

    except requests.exceptions.RequestException as e:
        if e.response:
            status_code = e.response.status_code
            detail = e.response.json()
            raise HTTPException(status_code=status_code, detail=detail)
    
    except Exception as e:
        logger.error(f"Unexpected error in line login profile: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

@linebot_router.get("/uri")
async def get_line_login_link(request: Request):
    try:
        r_uri = os.environ.get("LINE_LOGIN_URI")
        client_id = LINE_LOGIN_CHANNEL_ID
        state = secrets.token_urlsafe(16)
        line_auth_api = "https://access.line.me/oauth2/v2.1/authorize"

        uri = f"{line_auth_api}?response_type=code&client_id={client_id}&redirect_uri={r_uri}&state={state}&scope=profile%20openid&initial_amr_display=lineqr"

        redis_client.set(f"state:{state}","valid",ex=300)
        
        return {'result': uri}
    
    except RedisError as e:
        logger.error(f"Error in redis connection: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Redis error")

    except Exception as e:
        logger.error(f"Error in get_line_login_link: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@linebot_router.post("/auth")
async def get_callback_code(request: Request):
    try:
        data = await request.json()

        if not data:
            raise HTTPException(status_code=400, detail="Invalid JSON data")

        code = data.get("code")
        state = data.get("state")

        # 驗證必要參數
        if not code:
            logger.error(f"No code is found")
            raise HTTPException(status_code=400, detail="Missing code parameter")
        if not state:
            logger.error(f"No state is found")
            raise HTTPException(status_code=400, detail="Missing state parameter")
        
        if redis_client.exists(f"state:{state}") !=1:
            logger.error(f"Invalid state")
            raise HTTPException(status_code=401, detail="Invalid state")
    
        access_token = await get_line_login_token(code)

        if not access_token:
            return
        
        verified_response = await line_login_verify(access_token)

        if not verified_response:
            return
        
        profile:dict = await line_login_profile(access_token)
       
        if profile:
            token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            token = create_token(
                data={"id": profile['userId'], "name": profile["displayName"], "picture": profile["pictureUrl"]}, expires_delta=token_expires
            )
            user = LineUser(id=profile['userId'], name=profile["displayName"], pictureUrl=profile["pictureUrl"])
            await add_user(user)

            return Token(token=token, token_type="bearer")
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        logger.error(f"Unexpected error in auth: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))