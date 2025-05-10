import os
import aiohttp
from datetime import datetime
from zoneinfo import ZoneInfo

async def link_telegram_id(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{os.getenv('API_BASE_URL')}link_telegram_id/",
                json={"telegram_id": str(telegram_id)}
        ) as response:
            return response.status in (200, 201)

async def create_task(telegram_id, task_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{os.getenv('API_BASE_URL')}tasks/?telegram_id={telegram_id}",
                json=task_data
        ) as response:
            return response.status == 201

async def get_tasks(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{os.getenv('API_BASE_URL')}tasks/?telegram_id={telegram_id}") as response:
            if response.status == 200:
                data = await response.json()
                adak_tz = ZoneInfo("America/Adak")
                return [
                    {
                        "title": task["title"],
                        "description": task["description"],
                        "created_at": datetime.fromisoformat(task["created_at"]).astimezone(adak_tz).strftime("%Y-%m-%d %H:%M"),
                        "due_date": datetime.fromisoformat(task["due_date"]).astimezone(adak_tz).strftime("%Y-%m-%d %H:%M"),
                        "categories": [cat["name"] for cat in task["categories"]],
                        "completed": task["completed"]
                    } for task in data
                ]
            return []