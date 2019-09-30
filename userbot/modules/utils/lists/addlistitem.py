import re

from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import get_list, add_list
from . import DB_FAILED, CHK_HELP, LIST_NOT_FOUND


@register(outgoing=True, pattern=r"^.addlistitem(s)? ?(\w*)\n((.|\n*)*)")
async def add_list_items(event):
    """ For .addlistitems command, add item(s) to a list. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    textx = await event.get_reply_message()
    listname = None

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(2):
        listname = event.pattern_match.group(2)

    if not listname:
        return_msg = f"`Pass a list to add items into!` {CHK_HELP}"
        await event.edit(return_msg)
        return

    _list = await get_list(event.chat_id, listname)

    if not _list:
        await x.edit(LIST_NOT_FOUND.format(listname))

    content = _list['items']
    newitems = event.pattern_match.group(3)
    content.extend(newitems.splitlines())

    msg = "`Item(s) added successfully to the list.\n\n"
    msg += "New item(s):\n"
    msg += f"{newitems}\n\n"
    msg += f"Use` ${listname} `to get the list.`"

    if await add_list(event.chat_id, listname, content) is False:
        await event.edit(msg)
    else:
        await event.edit(LIST_NOT_FOUND.format(listname))
        return

    if BOTLOG:
        listat = "global storage" if _list['chat_id'] else str(event.chat_id)

        log = f"Added item(s) to {listname} in {listat}.\n"
        log += "New items:\n"
        log += f"{newitems}"

        await event.client.send_message(BOTLOG_CHATID, log)