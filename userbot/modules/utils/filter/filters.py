from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import get_filters


@register(outgoing=True, pattern="^.filters$")
async def filters_active(event):
    """ For .filters command, lists all of the active filters in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    transact = "`There are no filters in this chat.`"
    filters = await get_filters(event.chat_id)
    for filt in filters:
        if transact == "`There are no filters in this chat.`":
            transact = "Active filters in this chat:\n"
            transact += "🔹 **{}** - `{}`\n".format(filt["keyword"],
                                                    filt["msg"])
        else:
            transact += "🔹 **{}** - `{}`\n".format(filt["keyword"],
                                                    filt["msg"])

    await event.edit(transact)
