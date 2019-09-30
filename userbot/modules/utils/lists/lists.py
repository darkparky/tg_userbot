from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import get_lists, get_list
from . import NO_LISTS, DB_FAILED, LIST_HEADER, CHK_HELP


@register(outgoing=True, pattern="^.lists$")
async def lists_active(event):
    """ For .lists command, list all of the lists saved in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit(DB_FAILED)
        return

    message = NO_LISTS
    lists = await get_lists(event.chat_id)
    if lists.count() != 0:
        message = "Lists saved in this chat:\n"

        for _list in lists:
            message += "🔹 **{} ({})**\n".format(
                _list["name"], "Local" if
                (_list["chat_id"] != 0) else "Global")

    await event.edit(message)


@register(pattern=r"\$\w*",
          disable_edited=True,
          ignore_unsafe=True,
          disable_errors=True)
async def lists_logic(event):
    """ Lists logic. """
    try:
        if not (await event.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                return

            listname = event.text[1:]
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

                    return_str += f"\n{CHK_HELP}"
                else:
                    return_str = f"`This list is empty!` {CHK_HELP}"

                await event.reply(return_str)
    except BaseException:
        pass
