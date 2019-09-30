import re

from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import get_list, set_list
from . import DB_FAILED, CHK_HELP


@register(outgoing=True, pattern=r"^.setlist ?(\w*)? (global|local)")
async def setliststate(event):
    """ For .setlist command, changes the state of a list. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    _futureState = event.pattern_match.group(2)
    changeToGlobal = None

    if _futureState == "global":
        changeToGlobal = True
    elif _futureState == "local":
        changeToGlobal = False

    textx = await event.get_reply_message()
    listname = None

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list to remove!` {CHK_HELP}")
        return

    _list = await get_list(event.chat_id, listname)

    chatid = 0 if changeToGlobal else event.chat_id

    msg = f"`The state of list {listname} changed to \
{_futureState} successfully.`"

    if await set_list(_list['chat_id'], listname, chatid) is True:
        await event.edit(msg)
    else:
        await event.edit(f"`List {listname} not found!`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Changed state of list {listname} to {_futureState}")