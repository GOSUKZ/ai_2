# run_bot.py
import logging
import sys
import asyncio
from app.bot import bot, dp
from app.db.database import create_connection


async def main() -> None:
    create_connection()

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
