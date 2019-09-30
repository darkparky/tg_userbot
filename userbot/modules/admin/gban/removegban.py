from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import remove_chat_gban


@register(outgoing=True, pattern="^.removegban")
async def remove_from_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await remove_chat_gban(chat.chat_id)
    await chat.edit("`Removed this bot from the Gbanlist!`")
