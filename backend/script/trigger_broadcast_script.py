import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

from my_journalist.utils.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


def trigger_broadcast():
    url=f"{os.environ['BACKEND_URL']}/broadcast"

    token = os.getenv("API_TOKEN")

    payload = {"token":token}

    try:
        logger.info(f"📍 開始執行 trigger_broadcast")
        response = requests.post(url,json=payload)

        if 200 <=response.status_code <=299:
            logger.info("成功送出request to '/broadcast'")

        else:
            raise Exception(f"Failed to send request to '/broadcast'. Status code: {response.status_code}. Detail: {response.text}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    trigger_broadcast()