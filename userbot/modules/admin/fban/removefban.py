from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import remove_chat_fban


@register(outgoing=True, pattern="^.removefban")
async def remove_from_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await remove_chat_fban(chat.chat_id)
    await chat.edit("`Removed this chat from the Fbanlist!`")