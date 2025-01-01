import logging
import os
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import jwt
from fastapi import status

from my_journalist.database.config import settings
import redis
from redis import RedisError

from my_journalist.utils.logger import setup_logging
from my_journalist.routers.linebot import linebot_router
from my_journalist.routers.web_posts import web_posts_router
from my_journalist.routers.collcections import collcections_router
from my_journalist.routers.signup import signup_router
from my_journalist.routers.signin import signin_router
from my_journalist.utils.token_handler import decode_token

setup_logging()

logger = logging.getLogger(__name__)

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL")

public_routes = {"/uri", "/auth", "/broadcast", "/signup", "/signin"}
bearer_prefix = "Bearer "

try:
    redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    if redis_client.ping():
        redis_client.set("initialized", time.time())
        logger.info(f"Connected to Redis at {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    else:
        logger.error("Failed to ping Redis")
        raise ConnectionError("Failed to connect to Redis")
except ConnectionError:
    raise
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise e

if os.getenv("DEBUG") == "True":
    logger.info("Debug mode is enabled")   
    app = FastAPI(docs_url="/docs", redoc_url="/redoc")
else: 
    logger.info("Debug mode is disabled")
    app = FastAPI(docs_url=None, redoc_url=None)

@app.middleware("http")
async def auth_header(request: Request, call_next):
    path = request.url.path
    if path in public_routes:
        return await call_next(request)
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith(bearer_prefix):
        raise JSONResponse(status_code=401, content={"error": "Missing or invalid authorization header"})
    
    token = auth_header[len(bearer_prefix):]  # 使用偏移量提取 token
    try:
        decoded_token = decode_token(token)
        request.session["user_id"] = decoded_token['id']
        response = await call_next(request)
        return response

    except jwt.ExpiredSignatureError:
        logger.error(f"Token expired for path {path}")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"error": "Token expired"})

    except jwt.InvalidSignatureError:
        logger.error(f"Invalid signature for path {path}")
        raise JSONResponse(status_code=401, content={"error": "Invalid signature"})

  

app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_MIDDLEWARE_SECRET"),
    session_cookie="session",
    max_age=60*60,
    https_only=False,
    same_site="lax",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logging.error(f"HTTPException: {exc.detail}, status code: {exc.status_code}")
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

app.include_router(linebot_router)
app.include_router(web_posts_router)
app.include_router(collcections_router)
app.include_router(signup_router)
app.include_router(signin_router)


