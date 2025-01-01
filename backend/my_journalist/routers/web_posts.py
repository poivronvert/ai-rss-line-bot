import logging
import math
from fastapi import APIRouter, HTTPException, status, Query, Request

from my_journalist.utils.logger import setup_logging
from my_journalist.database.schemas import PostPayload
from my_journalist.database.crud import get_post_ids, select_article_by_id, get_article_number, get_posts_by_pagination
from my_journalist.database.schemas import ArticleResponse, ArticleDetails, PaginationResponse, PostDetail, TotalPages

setup_logging()

logger = logging.getLogger(__name__)

web_posts_router = APIRouter(prefix="/posts")    

@web_posts_router.get("/", response_model=PostDetail)
async def get_posts(request:Request,limit:int,offset:int):
    try:
        user_id = request.session.get("user_id")
        posts = await get_posts_by_pagination(user_id=user_id,limit=limit, offset=offset)
        return PostDetail(posts=posts)
    except Exception as e:
        logger.error(f"Failed to get posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get posts")
    
@web_posts_router.get("/totalpages", response_model=TotalPages)
async def get_totalpages(limit:int):
    try:
        totalNumber = get_article_number()
        totalPages = math.ceil(totalNumber / limit)
        return TotalPages(totalPages=totalPages)
    
    except Exception as e:
        logger.error(f"Failed to get total pages: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get total pages")

@web_posts_router.get("/{id}", response_model=ArticleDetails)
async def get_article_contents(request: Request, id):
    try:
        user_id = request.session.get("user_id")
        contents = await select_article_by_id(id,user_id)

        if contents is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        return contents
    except HTTPException as e:
        raise e
    
    except Exception as e:
        logger.error(f"Failed to get posts: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get posts")