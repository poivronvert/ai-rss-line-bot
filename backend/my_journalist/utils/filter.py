import os
import logging
import asyncio

from dotenv import load_dotenv
from openai import OpenAI

from my_journalist.database.crud import get_links, get_filtered_links

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def classify_relevance():
    contexts = get_links()
    system_prompt = '''You are a classifier determining text relevance to a specified topic. Respond with only 'Relevant' or 'Not Relevant' for each text.'''
    user_prompt = '''Is the following text relevant to Laboratory Information Management Systems (LIMS) or laboratory report management? Consider LIMS features, implementation, benefits, challenges, and aspects of managing laboratory reports.'''
    async def classify_single_text(item_id, item_text):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content":system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                    {
                        "role": "user",
                        "content":f"***UUID: {item_id}\n{item_text}"
                    },
                ],
            )
            response_text = completion.choices[0].message.content
            return item_id if response_text.strip().lower() == 'relevant' else None
        except Exception as e:
            logging.error(f"Error in classifying relevance single text {item_id}: {e}")
            return None
        
    try:
        tasks = [classify_single_text(item_id,item_text) for item_id, item_text in contexts.items()]
        results = await asyncio.gather(*tasks)
        return [result for result in results]
    
    except Exception as e:
        logging.error(f"Error in classifying relevance: {e}")

    
async def classify_category():
    filtered_contexts = get_filtered_links()
    categories = ["Engagement", "Public", "Compliance and Regulation", "Innovation", "Deals"]
    category_descriptions = {
        "Engagement": "Commercial activities aimed at building capacity and establishing collaborative agreements.",
        "Public": "Macro-level policies and commitments from national or government entities.",
        "Compliance and Regulation": "Specific laws, regulations, and regulatory requirements.",
        "Innovation": "Technologies or innovations that are still in the demonstration, research and development, or experimental stages.",
        "Deals": "Involves specific transactions such as mergers and acquisitions (M&A), strategic alliances, equity investments, and asset spin-offs."
    }
    system_prompt = f"Classify the following text into one of the categories: {', '.join(categories)}\n\n"
    for category, description in category_descriptions.items():
        system_prompt += f"{category}: {description}\n"
    system_prompt += "Respond with only category. If there is no proper category for the text, reply 'None'."
    user_prompt = '''Please help classify the text.'''
    async def classify_single_text(index, text):
        try: 
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role":"system",
                        "content":system_prompt,

                    },
                    {
                        "role":"user",
                        "content":user_prompt

                    },
                    {
                        "role": "user",
                        "content":f"***UUID: {index}\n{text}"
                    },
                ],
            )
            response_text = completion.choices[0].message.content
            if response_text not in categories:
                logging.warning(f"Error in classifying category single text {response_text}")
                return {"id":index,"category":None}
            return {"id":index,"category":response_text}
        except Exception as e:
            logging.error(f"Error in classifying category single text {index}: {e}")
            return None
        
    try:
        tasks = [classify_single_text(item_id, item_text) for item_id, item_text in filtered_contexts.items()]
        results = await asyncio.gather(*tasks)
        return [result for result in results]
    except Exception as e:
        logging.error(f"Error in classifying category: {e}")