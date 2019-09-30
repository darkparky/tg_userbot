import re

from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import get_list, delete_list
from . import DB_FAILED, CHK_HELP


@register(outgoing=True, pattern=r"^.rmlist ?(\w*)")
async def removelists(event):
    """ For .rmlist command, delete list with the given name."""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    textx = await event.get_reply_message()
    listname = None

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list to delete!` {CHK_HELP}")
        return

    _list = await get_list(event.chat_id, listname)

    if await delete_list(event.chat_id, listname) is False:
        await event.edit("`Couldn't find list:` **{}**".format(listname))
        return
    else:
        await event.edit("`Successfully deleted list:` **{}**".format(listname)
                         )

    if BOTLOG:
        listat = "global storage" if _list['chat_id'] == 0 else str(
            event.chat_id)
        await event.client.send_message(
            BOTLOG_CHATID, f"Removed list {listname} from {listat}")