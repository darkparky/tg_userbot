import re

from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import get_list, add_list
from . import DB_FAILED, LIST_NOT_FOUND, CHK_HELP


@register(outgoing=True, pattern=r"^\.editlistitem ?(\w*)? ([0-9]+) (.*)")
async def edit_list_item(event):
    """ For .editlistitem command, edit an individual item on a list. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    textx = await event.get_reply_message()

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list!` {CHK_HELP}")
        return

    item_number = int(event.pattern_match.group(2))

    _list = await get_list(event.chat_id, listname)
    content = _list['items']
    content[item_number - 1] = event.pattern_match.group(3)

    msg = f"`Item {item_number} edited successfully.\n"
    msg += f"Use` ${listname} `to get the list.`"

    if await add_list(event.chat_id, listname, content) is False:
        await event.edit(msg)
    else:
        await event.edit(LIST_NOT_FOUND.format(listname))

    if BOTLOG:
        listat = "global storage" if _list['chat_id'] else str(event.chat_id)

        log = f"Edited item {item_number} of "
        log += f"{listname} in {listat} successfully."
        await event.client.send_message(BOTLOG_CHATID, log)
