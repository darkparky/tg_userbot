from telethon.tl import functions

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.dc$")
async def neardc(event):
    """ For .dc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Country : `{result.country}` \n"
                     f"Nearest Datacenter : `{result.nearest_dc}` \n"
                     f"This Datacenter : `{result.this_dc}`")

add_help_item(
    ".dc",
    "Misc",
    "Get the nearest datacenter information.",
    """
    `.dc`
    """
)
