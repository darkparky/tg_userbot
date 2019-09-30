from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import add_list
from . import DB_FAILED


@register(outgoing=True, pattern=r"^.add(g)?list (\w*)")
async def addlist(event):
    """ For .add(g)list command, saves lists in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    is_global = event.pattern_match.group(1) == "g"

    listname = event.pattern_match.group(2)
    content = event.text.partition(f"{listname} ")[2].splitlines()

    msg = "`List {} successfully. Use` ${} `to get it.`"

    chatid = 0 if is_global else event.chat_id

    if await add_list(chatid, listname, content) is False:
        await event.edit(msg.format('updated', listname))
    else:
        await event.edit(msg.format('created', listname))

    if BOTLOG:
        listat = "global storage" if is_global else str(event.chat_id)
        await event.client.send_message(
            BOTLOG_CHATID, f"Created list {listname} in {listat}")
