from ...help import add_help_item
from userbot import is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.dbhelper import delete_sub


@register(outgoing=True, pattern=r"^\.rmsub\s+([\w\d]+)$")
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

add_help_item(
    ".rmsub",
    "Utilities",
    "Remove a subscription.",
    """
    `.rmsub (name)`
    """
)