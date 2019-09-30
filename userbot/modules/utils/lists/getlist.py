import re

from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import get_list
from . import CHK_HELP, LIST_HEADER


@register(pattern=r"^.getlist ?(\w*)?")
async def getlist_logic(event):
    """ For .getlist, get the list by the name. """
    if not (await event.get_sender()).bot:
        if not is_mongo_alive() or not is_redis_alive():
            return

        textx = await event.get_reply_message()

        if textx:
            x = re.search(r"\[Paperplane-List] List \*\*(\w*)", textx.text)
            listname = x.group(1)
        elif event.pattern_match.group(1):
            listname = event.pattern_match.group(1)
        else:
            await event.edit(f"`Pass a list to get!` {CHK_HELP}")
            return

        _list = await get_list(event.chat_id, listname)
        if _list:
            if _list['chat_id'] == 0:
                storage = "global"
            else:
                storage = str(_list['chat_id'])

            return_str = LIST_HEADER.format(listname, storage)

            if _list['items']:
                for i, item in enumerate(_list['items']):
                    return_str += f"{i + 1}. {item}\n"
            else:
                return_str = "`This list is empty!`"

            await event.edit(return_str)
        else:
            await event.edit(f"`List {listname} not found!`")
