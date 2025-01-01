import sys
import json
import logging
from datetime import datetime
import uuid
from collections import defaultdict
from typing import Optional, Dict, List
import bcrypt

import pkgutil
from sqlalchemy import select, func, and_, exc, exists, or_
import asyncio

from my_journalist.utils.parser import parse_rss, parse_html
from my_journalist.database.models import (
    Rss,
    Link,
    FilteredLink,
    Article,
    User,
    Collection,
)
from my_journalist.database.db import SessionLocal
from my_journalist.utils.logger import setup_logging
from my_journalist.database.schemas import UserSignin

setup_logging()

logger = logging.getLogger(__name__)


def add_rss(source: str, url: str):

    logger.info("進入add_rss")

    try:
        with SessionLocal() as session:
            rss = Rss(id=str(uuid.uuid4()), source=source, url=url)
            session.add(rss)
            session.commit()

    except Exception as e:
        logger.error(f"{e}", exc_info=True)


def init_rss():
    new_source_count = 0

    data = pkgutil.get_data("my_journalist", "data/init_rss_data.json")
    if data is None:
        logger.warning("No initial RSS data found")
        return

    json_data = json.loads(data.decode("utf-8"))

    try:
        with SessionLocal() as session:
            existed_rss = session.execute(select(Rss.url)).scalars().all()

        for source, url in json_data.items():
            if url not in existed_rss:
                add_rss(source, url)
                new_source_count += 1

    except Exception as e:
        logger.error(f"{e}", exc_info=True)


async def get_rss():
    try:
        with SessionLocal() as session:
            rss_list = session.execute(select(Rss)).scalars().all()

            tasks = [
                add_link(await parse_rss({rss.source: rss.url})) for rss in rss_list
            ]

            await asyncio.gather(*tasks)

            for rss in rss_list:
                rss.fetched_at = datetime.now()

            session.commit()

    except Exception as e:
        logger.error(f"Error in getting rss: {e}", exc_info=True)


async def add_link(rss_content: list[dict]) -> None:
    try:
        with SessionLocal() as session:

            existing_links = session.execute(select(Link.link)).scalars().all()

            new_links = [
                Link(
                    id=str(uuid.uuid4()),
                    source=data["source"],
                    title=data["title"],
                    link=data["link"],
                    published_at=data["published_at"],
                    created_at=datetime.now(),
                )
                for data in rss_content
                if data["link"] not in existing_links
            ]

            if new_links:
                session.add_all(new_links)
                session.commit()

    except Exception as e:
        logger.error(f"Error in adding link: {e}", exc_info=True)


async def add_link_text() -> None:
    try:
        with SessionLocal() as session:
            stmt = select(Link).where(
                and_(
                    func.date(Link.created_at) == datetime.today().date(),
                    Link.text == "",
                )
            )
            links = session.execute(stmt).scalars().all()
            for link in links:
                if link.link is not None:
                    readable_context = await parse_html(link.link)
                    if readable_context is not None:
                        link.text = readable_context
            session.commit()
    except Exception as e:
        logger.error(f"Error in adding text: {e}", exc_info=True)


def get_links() -> dict:
    try:
        condition = func.date(Link.created_at) == datetime.today().date()
        with SessionLocal() as session:
            results = session.execute(select(Link.id, Link.text).where(condition)).all()
        return {str(id): text for id, text in results}

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


def add_filtered_link(relevant_uuids: list) -> None:
    try:
        with SessionLocal() as session:
            links = (
                session.execute(select(Link).where(Link.id.in_(relevant_uuids)))
                .scalars()
                .all()
            )
            filtered_links = [
                FilteredLink(
                    id=str(uuid.uuid4()),
                    source=link.source,
                    title=link.title,
                    link=link.link,
                    text=link.text,
                    created_at=datetime.now(),
                )
                for link in links
            ]
        session.add_all(filtered_links)
        session.commit()
    except Exception as e:
        logger.error(f"Error in adding filtered link{e}", exc_info=True)


def get_filtered_links() -> dict:
    condition = func.date(FilteredLink.created_at) == datetime.today().date()

    try:
        with SessionLocal() as session:
            results = session.execute(
                select(FilteredLink.id, FilteredLink.text).where(condition)
            ).all()

        return {str(id): text for id, text in results}

    except Exception as e:
        logger.error(f"Error in getting filtered links {e}", exc_info=True)


def update_category(filtered_cat: list[dict]):
    try:
        with SessionLocal() as session:
            for item in filtered_cat:
                target = session.execute(
                    select(FilteredLink).where(FilteredLink.id == item["id"])
                ).scalar()
                target.category = item["category"]
            session.commit()
    except Exception as e:
        logger.error(f"Error in updating category {e}", exc_info=True)


def get_text_and_cat():
    condition = and_(
        FilteredLink.category != None,
        func.date(FilteredLink.created_at) == datetime.today().date(),
    )

    try:
        with SessionLocal() as session:
            results = session.execute(
                select(FilteredLink.text, FilteredLink.category).where(condition)
            ).all()

            if not results:
                logger.info("FilteredLink資料庫沒有相關內容")
                return {}

            category_dict = defaultdict(list)
            for text, category in results:
                category_dict[category].append(text)
            return dict(category_dict)
    except Exception as e:
        logger.error(f"Error in getting text and category {e}", exc_info=True)


def add_article(summary: dict):
    try:
        with SessionLocal() as session:
            title = (
                "本日無新增相關新聞"
                if not summary
                else f"每日更新 {datetime.today().year}.{datetime.today().month}.{datetime.today().day}"
            )
            new_article = Article(
                id=str(uuid.uuid4()),
                title=title,
                engagement=summary.get("Engagement", ""),
                public=summary.get("Public", ""),
                regulation=summary.get("Compliance and Regulation", ""),
                innovation=summary.get("Innovation", ""),
                deals=summary.get("Deals", ""),
                created_at=datetime.now(),
            )
            session.add(new_article)
            session.commit()

    except Exception as e:
        logger.error(f"Error in adding article {e}", exc_info=True)


async def get_today_article():
    try:
        condition = func.date(Article.created_at) == datetime.today().date()

        with SessionLocal() as session:
            results = session.execute(select(Article).where(condition)).first()

            response = []
            for item in results:
                items = [
                    value
                    for value in [
                        item.id,
                        item.title,
                        item.engagement,
                        item.public,
                        item.regulation,
                        item.innovation,
                        item.deals,
                    ]
                    if value != ""
                ]
                response.extend(items)
            return response

    except exc.OperationalError as e:
        # Log the error and retry after a short delay
        logger.error(f"Database connection error: {e}")
        await asyncio.sleep(1)
        return await get_today_article()

    except Exception as e:
        logger.error(f"Error in getting article {e}", exc_info=True)


def get_post_ids():
    try:
        with SessionLocal() as session:
            results = session.execute(select(Article)).scalars().all()

            posts = [{"id": str(result.id)} for result in results]

            return posts
    except Exception as e:
        logger.error(f"Error in getting article {e}", exc_info=True)


async def select_article_by_id(article_id: str, user_id: str) -> Optional[Dict]:
    with SessionLocal() as session:
        # 建立子查詢來檢查文章是否在收藏中
        collection_exists = exists(
            select(1)
            .select_from(Collection)
            .where(
                and_(
                    Collection.user_id == user_id,
                    Collection.article_id == Article.id,
                )
            )
        ).label("in_collection")
        
        # 主查詢
        query = select(
            Article,
            FilteredLink.category,
            FilteredLink.link,
            collection_exists
        ).where(
            and_(
                Article.id == article_id,
                func.date(Article.created_at) == func.date(FilteredLink.created_at),
            )
        )
        
        results = session.execute(query).all()
        
        if not results:
            # 如果沒有找到 FilteredLinks，只查詢文章基本信息
            article_query = select(Article).where(Article.id == article_id)
            article_result = session.execute(article_query).first()
            
            if article_result:
                article = article_result[0]
                return {
                    "title": article.title,
                    "engagement": None,
                    "public": None,
                    "regulation": None,
                    "innovation": None,
                    "deals": None,
                    "links": {},
                    "in_collection": False
                }
            return None
            
        # 解構查詢結果
        first_row = results[0]
        article: Article = first_row.Article
        is_in_collection: bool = first_row.in_collection
        
        # 整理链接
        links: Dict[str, List[str]] = defaultdict(list)
        for row in results:
            links[row.category].append(row.link)
        
        return {
            "title": article.title,
            "engagement": article.engagement,
            "public": article.public,
            "regulation": article.regulation,
            "innovation": article.innovation,
            "deals": article.deals,
            "links": dict(links),
            "in_collection": is_in_collection,
        }


def get_article_number():
    try:
        with SessionLocal() as session:
            totoalnumber = session.execute(
                select(func.count(Article.id)).where(
                    Article.title != "本日無新增相關新聞"
                )
            ).scalar()

            return totoalnumber
    except Exception as e:
        logger.error(f"Error in getting article {e}", exc_info=True)


async def get_posts_by_pagination(user_id: str, limit: int, offset: int):
    with SessionLocal() as session:
        collection_count_subquery = (
            select(func.count(Collection.id))
            .where(Collection.article_id == Article.id)
            .correlate(Article)  # 確保子查詢與 Article 關聯
            .scalar_subquery()
        )

        query = (
            select(
                Article.id,
                Article.title,
                exists(
                    select(1)
                    .select_from(Collection)
                    .where(
                        and_(
                            Collection.user_id == user_id,
                            Collection.article_id == Article.id,
                        )
                    )
                ).label("in_collection"),
                collection_count_subquery.label("collection_count"),
            )
            .where(Article.title != "本日無新增相關新聞")
            .order_by(Article.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        results = session.execute(query).mappings().all()

        posts = [
            {
                "id": str(result["id"]),
                "name": result["title"],
                "in_collection": result["in_collection"],
                "collection_count": result["collection_count"],
            }
            for result in results
        ]

        return posts

async def add_user(user: User):
    try:
        with SessionLocal() as session:
            conditions = [User.id == user.id]
            if hasattr(user, 'email') and user.email:
                conditions.append(User.email == user.email)
            query = select(func.count(User.id)).where(or_(*conditions))
            num = session.execute(query).scalar()
            if num > 0:
                return False
            else:
                session.add(user)
                session.commit()
                return True
    except Exception as e:
        logger.error(f"Error in adding user {e}", exc_info=True)
        raise

async def check_user_logged_in(user:UserSignin):
    try:
        with SessionLocal() as session:
            verify_email = session.execute(
                select(User).where(User.email == user.email)
            ).scalar_one_or_none()
            verify_password = bcrypt.checkpw(user.password.encode(), verify_email.password.encode())

            if not verify_email or not verify_password:
                return False
            data = {
                "id": verify_email.id,
                "name": verify_email.name,
            }
            return data
    except Exception as e:
        logger.error(f"Error in checking user logged in: {e}", exc_info=True)
        raise

async def check_collection_status(user_id: str, article_id: str):
    try:
        with SessionLocal() as session:
            num = session.execute(
                select(func.count(Collection.id)).where(
                    and_(
                        Collection.user_id == user_id,
                        Collection.article_id == article_id,
                    )
                )
            ).scalar()
            return num > 0

    except Exception as e:
        logger.error(f"Error in checking collection status: {e}", exc_info=True)
        raise

async def add_collection(user_id: str, article_id: str):
    try:
        is_collected = await check_collection_status(user_id, article_id)
        if is_collected:
            return

        with SessionLocal() as session:
            new_collection = Collection(
                id=str(uuid.uuid4()), user_id=user_id, article_id=article_id
            )
            session.add(new_collection)
            session.commit()
            return True
    except Exception as e:
        logger.error(f"Error in updating collection: {e}", exc_info=True)
        raise e

async def delete_collection(user_id: str, article_id: str):
    try:
        is_collected = await check_collection_status(user_id, article_id)
        if not is_collected:
            return

        with SessionLocal() as session:
            session.query(Collection).filter(
                and_(Collection.user_id == user_id, Collection.article_id == article_id)
            ).delete()
            session.commit()
            return True

    except Exception as e:
        logger.error(f"Error in updating collection: {e}", exc_info=True)
        raise e

if __name__ == "__main__":
    print(asyncio.run(select_article_by_id(user_id="Uf104d0f60af2784736a6ad7ddc03bff0", article_id="b75d1e34-a222-4632-9dd4-831411b7f386")))