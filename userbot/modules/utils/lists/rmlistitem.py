import re

from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import get_list, add_list
from . import DB_FAILED, CHK_HELP, LIST_NOT_FOUND


@register(outgoing=True, pattern=r"^.rmlistitem ?(\w*)? ([0-9]+)")
async def rmlistitems(event):
    """ For .rmlistitem command, remove an item from the list. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    await event.edit("`Removing...`")

    textx = await event.get_reply_message()

    if textx:
        x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
        listname = x.group(1)
    elif event.pattern_match.group(1):
        listname = event.pattern_match.group(1)
    else:
        await event.edit(f"`Pass a list to remove items from!` {CHK_HELP}")
        return

    item_number = int(event.pattern_match.group(2))

    _list = await get_list(event.chat_id, listname)

    try:
        content = _list['items']
        del content[item_number - 1]
    except TypeError:
        await event.edit(LIST_NOT_FOUND.format('listname'))
        return
    except IndexError:
        await event.edit(f"`Item `**{item_number}**\
` in list `**{listname}**` not found!`")
        return

    msg = "`Item {} removed from the list successfully. \
Use` ${} `to get the list.`"

    if await add_list(event.chat_id, listname, content) is False:
        await event.edit(msg.format(item_number, listname))
    else:
        await event.edit(f"List {listname} doesn't exist!")

    if BOTLOG:
        listat = "global storage" if _list['chat_id'] else str(event.chat_id)
        await event.client.send_message(
            BOTLOG_CHATID,
            f"Removed item {str(item_number)} from {listname} in {listat}")
