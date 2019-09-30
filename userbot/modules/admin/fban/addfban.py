from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import add_chat_fban


@register(outgoing=True, pattern="^.addfban")
async def add_to_fban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await add_chat_fban(chat.chat_id)
    await chat.edit("`Added this chat under the Fbanlist!`")