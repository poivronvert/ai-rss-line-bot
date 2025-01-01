import os
import logging

from dotenv import load_dotenv
import feedparser
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from dateutil import parser
from dateutil.tz import gettz

from my_journalist.utils.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

load_dotenv()
async def fetch_feed(rss_url:str) -> dict:
    """
    Fetch a RSS feed from a given URL, and parse it into a dictionary object.

    Args:
        rss_url (str): The URL of the RSS feed to fetch.

    Returns:
        dict: A dictionary object containing the parsed RSS feed.
    """
    try:
        async with ClientSession() as session:
            async with session.get(rss_url, headers={'User-Agent': os.getenv('USER_AGENT')}) as response:
                content = await response.read()
                parsed_feed = feedparser.parse(content)
                return parsed_feed
    except Exception as e:
        logger.error(f"Error in fetching feed: {e}")
        
async def parse_rss(news_url: dict[str, str]) -> list:
    """
    Parse the RSS feeds from a given dictionary of source name to URL.

    Args:
        news_url (dict[str, str]): A dictionary object containing the source name as the key and the RSS feed URL as the value.

    Returns:
        list[dict]: A list of dictionaries containing the parsed RSS feed.
    """
    rss_content = []
    for source, url in news_url.items():
        try: 
            parsed_results = await fetch_feed(url)
            rss_content.extend(
                [
                    {
                        "source": source,
                        "title": entry["title"],
                        "link": entry["link"],
                        "published_at": parser.parse(entry["published"], tzinfos={"EDT": gettz("US/Eastern")}),
                    }
                    for entry in parsed_results["entries"]
                ]
            )

            logger.info(f"Parsed {len(parsed_results['entries'])} entries from {source}")

        except Exception as e:
            logger.error(f"Error parsing RSS feed from {source}: {str(e)}")
            
    return rss_content

async def parse_html(link:str) -> str: 
    """
    Fetch the content of a given URL, and parse it into a plain text using BeautifulSoup.

    Args:
        link (str): The URL of the content to fetch.

    Returns:
        str: The parsed content as plain text.
    """
    try: 
        async with ClientSession() as session:
            async with session.get(link, headers={'User-Agent': os.getenv('USER_AGENT')}) as response:
                html_content = await response.text()
                soup = BeautifulSoup(html_content, "html.parser")
                readable_text = soup.get_text(strip=True)

        return readable_text
    except Exception as e:
        logger.error(f"Error in parsing html: {e}")