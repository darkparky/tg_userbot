from platform import python_version

from telethon import version

from userbot import is_mongo_alive, is_redis_alive, bot
from userbot.events import register
from userbot.modules import ALL_MODULES


@register(outgoing=True, pattern="^.alive$")
async def amireallyalive(e):
    if not is_mongo_alive() and not is_redis_alive():
        db = "Both Mongo and Redis Database seems to be failing!"
    elif not is_mongo_alive():
        db = "Mongo DB seems to be failing!"
    elif not is_redis_alive():
        db = "Redis Cache seems to be failing!"
    else:
        db = "Databases functioning normally!"

    username = (await bot.get_me()).username
    await e.edit("`"
                 "Your bot is running \n\n"
                 f"Telethon version: {version.__version__} \n"
                 f"Python: {python_version()} \n"
                 f"User: @{username} \n"
                 f"Database Status: {db} \n"
                 f"Modules loaded: {len(ALL_MODULES)}"
                 "`")
