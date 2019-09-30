from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import add_chat_gban


@register(outgoing=True, pattern="^.addgban")
async def add_to_gban(chat):
    if not is_mongo_alive() or not is_redis_alive():
        await chat.edit("`Database connections failing!`")
        return
    await add_chat_gban(chat.chat_id)
    print(chat.chat_id)
    await chat.edit("`Added this bot under the Gbanlist!`")