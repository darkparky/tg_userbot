from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import get_subs
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^.subs\s?(.*)?$")
async def list_subscriptions(event):
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`", delete_in=3)
        return

    params = event.pattern_match.group(1) or ""
    args, _ = parse_arguments(params, ['all'])

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
