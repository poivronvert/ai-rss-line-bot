import os
import logging

from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from my_journalist.utils.logger import setup_logging
from my_journalist.database.crud import add_collection, check_collection_status, delete_collection

setup_logging()

logger = logging.getLogger(__name__)

load_dotenv()

collcections_router = APIRouter(
    prefix="/collections",
    tags=["collections"],
)

@collcections_router.get("/")
async def get_collection_status(request: Request, article_id: str):
    try:
        user_id = request.session.get("user_id")
        logger.info(f"使用者 {user_id} 查詢文章：{article_id}")
        is_collected = await check_collection_status(article_id=article_id, user_id=user_id)
        return {"exists": is_collected}
    except Exception as e:
        logger.error(f"Error in getting collection status: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get collection status")

@collcections_router.post("/add")
async def add_to_collection(request: Request, payload:dict):
    try:
        user_id = request.session.get("user_id")
        article_id = payload["article_id"]
        await add_collection(article_id=article_id, user_id=user_id)
        return {"message": "Article added to collection"}
    except Exception as e:
        logger.error(f"Error in adding to collection: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add to collection")

@collcections_router.delete("/delete")
async def remove_from_collection(request: Request, payload:dict):
    try:
        user_id = request.session.get("user_id")
        article_id = payload["article_id"]
        await delete_collection(article_id=article_id, user_id=user_id)
        return {"message": "Article removed from collection"}
    except Exception as e:
        logger.error(f"Error in removing from collection: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to remove from collection")