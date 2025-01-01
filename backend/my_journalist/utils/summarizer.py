import os
import logging

import asyncio
from openai import OpenAI
from dotenv import load_dotenv 

from my_journalist.database.crud import get_text_and_cat


load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def generate_summary():
    category_dict = get_text_and_cat()

    if not category_dict:
        return {}

    async def generate_digest(*texts) -> str:
        if not texts:
            return ""
        articles = (
            "\n\n\n\n\n----------------NEXT Content----------------\n\n\n\n\n\n".join(
                texts
            )
        )
        try: 
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"以下是一系列文章的總結，請幫我把這些內容概述為繁體中文且不要包含任何標題標示符號（例如：**或#）。\n\n{articles}",
                    }
                ],
            )
            response = completion.choices[0].message.content
            return response
        except Exception as e:
            logging.error(f"Error in generating digest {e}")
            return ""
    try:
        tasks ={category: asyncio.create_task(generate_digest(*texts)) for category,texts in category_dict.items()}
        results = {}
        for category, task in tasks.items():
            try:
                result = await task
                if result:
                    results[category] = result
            except Exception as e:
                logging.error(f"Error in generating digest for category {category}: {e}")
        return results
    except Exception as e:
        logging.error(f"Error in generating summary {e}")