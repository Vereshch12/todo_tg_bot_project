import os
import aiohttp
import logging

logger = logging.getLogger(__name__)

async def send_telegram_notification(telegram_id: str, message: str):
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("BOT_TOKEN is not set")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": message,
        "parse_mode": "HTML"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                logger.info(f"Notification sent to {telegram_id}: {message}")
                return True
            else:
                logger.error(f"Failed to send notification to {telegram_id}: {await response.text()}")
                return False