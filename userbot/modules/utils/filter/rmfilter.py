from ...help import add_help_item
from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import delete_filter


@register(outgoing=True, pattern="^.rmfilter\\s.*")
async def remove_filter(event):
    """ Command for removing a filter """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    filt = event.text[6:]

    if BOTLOG:
        if not await delete_filter(event.chat_id, filt):
            await event.client.send_message(
                BOTLOG_CHATID,
                "`Filter` **{}** `doesn't exist.`".format(filt))
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "`Filter` **{}** `was deleted successfully`".format(filt))
    await event.delete()

add_help_item(
    ".rmfilter",
    "Utilities [filters]",
    "Remove a filter.",
    """
    `.rmfilter "(pattern)"`
    """
)