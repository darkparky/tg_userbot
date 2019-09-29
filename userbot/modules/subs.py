from datetime import timedelta
from asyncio import sleep
from re import match

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.utils.helpers import parse_arguments
from userbot.modules.dbhelper import (
    get_sub, get_subs, add_sub, delete_sub)

@register(outgoing=True, pattern=r".sub ([\S\s]+)")
async def add_subscription(e):
    """ Add a subscription pattern. Whenever this pattern
    is matched in the current chat you will be notified """
    params = e.pattern_match.group(1)

    if not is_mongo_alive() or not is_redis_alive():
        await e.edit("`Database connections failing!`", delete_in=3)
        return
    
    args, pattern = parse_arguments(params)
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

        
@register(outgoing=True, pattern=r"^.subs\s?(.*)?$")
async def list_subscriptions(event):
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`", delete_in=3)
        return

    params = event.pattern_match.group(1) or ""
    args, _ = parse_arguments(params)

    fetch_all = args.get('all', False)

    await event.edit("Fetching subscriptions...")
    if fetch_all:
        subs = list(await get_subs(None))
    else:    
        subs = list(await get_subs(event.chat_id))

    message = "**Subscribed patterns** \n"
    if len(subs) < 1:
        message += "No subscriptions yet."
    else:
        for sub in subs:
            gbl = '(g)' if sub['global'] else ''
            pattern = sub['pattern']
            pattern = pattern[:25] + (pattern[25:] and '..')
            message += f"`{sub['name']}{gbl}`: `{pattern}` \n"

    await event.edit(message.strip())

@register(outgoing=True, pattern=r"^.rmsub ([\w\d]+)$")
async def remove_subscription(event):
    if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`", delete_in=3)
            return

    name = event.pattern_match.group(1)
    await event.edit("Removing subscription...")
    if await delete_sub(name):
        await event.edit("Subscription removed!", delete_in=3)
    else:
        await event.edit("A subscription with that name doesn't exist", delete_in=3)

@register(pattern=r"([\S\s]+)",
          disable_edited=True,
          ignore_unsafe=True,
          disable_errors=True)
async def note(event):
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

CMD_HELP["General"].update({
    "sub":
        "Subscribes to a pattern in the current "
        "chat or globally. \n"
        "Usage: `.sub [global:bool]? (pattern)`",
    "rmsub":
        "Removes a sub by ID. \n"
        "Usage: `.rmsub (id)`",
    "subs":
        "List all subs for the current chat "
        "(including globals). \n"
        "Usage: `.subs`"
})