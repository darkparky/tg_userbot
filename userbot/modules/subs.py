from datetime import timedelta
from asyncio import sleep
from re import match

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.utils.helpers import parse_arguments
from userbot.modules.dbhelper import (
    get_sub, get_subs, add_sub, delete_sub)

@register(outgoing=True, pattern=r".sub ([\S\s]+)")
async def add_subscription(event):
    """ Add a subscription pattern. Whenever this pattern
    is matched in the current chat you will be notified """
    pattern = event.pattern_match.group(1)

    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    
    args, pattern = parse_arguments(pattern)
    await event.edit(f"Subscribing to pattern `{pattern}`")
    gbl = args.get('global', False)

    existing = bool(await get_sub(event.chat_id, pattern))
    if existing:
        # This pattern already exists, so we'll ignore.
        return

    if await add_sub(event.chat_id, pattern, gbl) is True:
        await event.edit("Added subscription!")
    
    sleep(1)
    await event.delete()
        
@register(outgoing=True, pattern=r"^.subs$")
async def list_subscriptions(event):
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return

    await event.edit("Fetching subscriptions...")
    subs = list(await get_subs(event.chat_id))

    message = "**Subscribed patterns** \n"
    if len(subs) < 1:
        message += "No subscriptions yet."
    else:
        for sub in subs:
            pattern = sub['pattern']
            pattern = pattern[:25] + (pattern[25:] and '..')
            message += f"`{sub['id']}`: `{pattern}` \n"

    await event.edit(message.strip())

@register(outgoing=True, pattern=r"^.rmsub ([\w\d]+)$")
async def remove_subscription(event):
    if not is_mongo_alive() or not is_redis_alive():
            await event.edit("`Database connections failing!`")
            return

    sub_id = event.pattern_match.group(1)
    await event.edit("Removing subscription...")
    await delete_sub(sub_id)
    await event.edit("Subscription removed!")
    
    sleep(1)
    await event.delete()

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
                    if event.chat.username and BOTLOG:
                        message_link = f"https://t.me/{event.chat.username}/{event.message.id}"
                        await event.client.send_message(
                            BOTLOG_CHATID,
                            f"Sub `{sub['id']}` triggered. Here's a link. \n{message_link}",
                            schedule=timedelta(seconds=3))
                    else:
                        await event.client.send_message(
                            event.chat_id,
                            f"Mentioning myself @{me.username}. Don't mind me.",
                            schedule=timedelta(seconds=3))
                    break
    except BaseException:
        pass