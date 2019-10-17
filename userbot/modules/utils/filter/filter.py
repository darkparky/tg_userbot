import re

from ...help import add_help_item
from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import add_filter, get_filters


@register(outgoing=True, pattern=r'^.filter\s+(?:"(.*)")?(\S+)?\s+([\S\s]+)')
async def add_new_filter(event):
    """ Command for adding a new filter """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    keyword = event.pattern_match.group(1) or event.pattern_match.group(2)
    string = event.pattern_match.group(3)

    if event.reply_to_msg_id:
        string = " " + (await event.get_reply_message()).text

    msg = "`Filter` **{}** `{} successfully`"

    if BOTLOG:
        if await add_filter(event.chat_id, keyword, string) is True:
            await event.client.send_message(
                BOTLOG_CHATID,
                msg.format(keyword, 'added'))
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                msg.format(keyword, 'updated'))
    event.delete()


@register(incoming=True, disable_edited=True, disable_errors=True)
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            if not is_mongo_alive() or not is_redis_alive():
                await handler.edit("`Database connections failing!`")
                return
            incoming_message = handler.text
            filters = await get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pro = re.fullmatch(trigger["keyword"],
                                   incoming_message,
                                   flags=re.IGNORECASE)
                if pro:
                    await handler.reply(trigger["msg"])
                    return
    except AttributeError:
        pass

add_help_item(
    ".filter",
    "Utilities",
    "Add a new filter. Filters allow you to respond "
    "to a specific pattern with a message.",
    """
    `.filter "(pattern)" (response)`
    """
)