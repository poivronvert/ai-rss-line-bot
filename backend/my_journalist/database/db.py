import logging

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
import redis

from redis.exceptions import RedisError

from my_journalist.database.config  import settings
from my_journalist.utils.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


engine = create_engine(
    settings.DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
