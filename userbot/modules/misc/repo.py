from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit("https://github.com/watzon/tg_userbot/")

add_help_item(
    ".repo",
    "Misc",
    "Returns the repo URL for this bot.",
    """
    `.repo`
    """
)
