#! /usr/local/env python3
import asyncio
import time
import logging
from my_journalist.database.crud import get_rss, add_link_text, add_filtered_link, update_category, add_article
from my_journalist.utils.filter import classify_relevance, classify_category
from my_journalist.utils.summarizer import generate_summary
from my_journalist.utils.logger import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

async def main():
    try:
        logger.info(f"📍 開始執行 get_rss()")
        await get_rss()

        logger.info(f"📍 開始執行 add_link_text()")
        await add_link_text()

        logger.info("📍 開始執行 classify_relevance()")
        results = await classify_relevance()

        logger.info("📍 開始執行 add_filtered_link()")
        add_filtered_link(results)

        logger.info("📍 開始執行 classify_category()")
        categorized_results = await classify_category()
        logger.info(f"已獲得類別分類結果，共 {len(categorized_results)} 條")

        logger.info("📍 開始執行 update_category()")
        update_category(categorized_results)

        logger.info("📍 開始執行 generate_summary()")
        summary_dict = await generate_summary()
        logger.info(f"已生成摘要，共 {len(summary_dict)} 條")

        logger.info("📍 開始執行 add_article()")
        add_article(summary_dict)

    except Exception as e:
        logger.error(f"❌ main() 過程中發生錯誤: {e}", exc_info=True)

if __name__ == "__main__":
    start_time = time.time()

    try:
        asyncio.run(main())
    
    except Exception as e:
        logger.error(f"❌ asyncio.run(main()) 失敗: {e}", exc_info=True)
        
    end_time = time.time()
    execution_time = end_time - start_time
    logger.info(f"執行時間: {execution_time:.4f} 秒")