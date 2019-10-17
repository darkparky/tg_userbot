from datetime import timedelta
from re import match

from ...help import add_help_item
from userbot import is_mongo_alive, is_redis_alive, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.dbhelper import add_sub, get_subs
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r".sub\s+([\S\s]+)")
async def add_subscription(e):
    """ Add a subscription pattern. Whenever this pattern
    is matched in the current chat you will be notified """
    params = e.pattern_match.group(1)

    if not is_mongo_alive() or not is_redis_alive():
        await e.edit("`Database connections failing!`", delete_in=3)
        return

    args, pattern = parse_arguments(params, ['global'])
    parts = pattern.split(' ')

    if not len(parts) >= 2:
        await e.edit("A name and pattern are required.", delete_in=3)
        return

    name = parts[0]
    pattern = ' '.join(parts[1:])

    await e.edit(f"Subscribing to pattern `{pattern}`")
    gbl = args.get('global', False)

    if await add_sub(e.chat_id, name, pattern, gbl=gbl) is True:
        if not args.get('silent'):
            await e.edit(f"Added subscription `{name}` for pattern `{pattern}`", delete_in=3)
        else:
            await e.edit("A subscription with that name already exists", delete_in=3)


@register(pattern=r"([\S\s]+)",
          disable_edited=True,
          disable_errors=True)
async def sub_logic(event):
    """ Subs logic. """
    try:
        me = await event.client.get_me()
        if not (await event.get_sender()).bot and not (event.from_id == me.id):
            if not is_mongo_alive() or not is_redis_alive():
                return

            subs = list(await get_subs(event.chat_id))

            for sub in subs:
                if match(sub['pattern'], event.text):
                    if event.chat.username:
                        message_link = f"https://t.me/{event.chat.username}/{event.message.id}"

                    else:
                        message_link = f"https://t.me/c/{event.chat_id}/{event.message.id}"

                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"Sub `{sub['name']}` triggered in chat `{event.chat_id}`. "
                        f"Here's a link. \n{message_link}",
                        schedule=timedelta(seconds=5))
                    break
    except BaseException:
        pass

add_help_item(
    ".sub",
    "Utilities",
    "Add a subscription, allowing you to be notified "
    "whenever a message matches a specific pattern.",
    """
    `.sub [options] (name) (pattern)`
    
    Options:
    `.global`: Use this subscription with all chats.
    """
)
