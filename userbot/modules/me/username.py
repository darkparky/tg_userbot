from telethon.errors import UsernameOccupiedError, UsernameInvalidError
from telethon.tl.functions.account import UpdateUsernameRequest

from ..help import add_help_item
from userbot import bot
from userbot.events import register

USERNAME_SUCCESS = "```Your username was successfully changed.```"
USERNAME_TAKEN = "```This username is already taken.```"
USERNAME_INVALID = "```Nobody is using this username, or the username is unacceptable. If the latter, it must match r\"[a-zA-Z][\w\d]{3,30}[a-zA-Z\d]\"```"


@register(outgoing=True, pattern=r"^\.username (.*)")
async def update_username(username):
    """ For .username command, set a new username in Telegram. """
    newusername = username.pattern_match.group(1)
    try:
        await bot(UpdateUsernameRequest(newusername))
        await username.edit(USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await username.edit(USERNAME_TAKEN)
    except UsernameInvalidError:
        await username.edit(USERNAME_INVALID)


add_help_item(
    ".username",
    "Me",
    "Set your username.",
    """
    `.username (new username)`
    """
)
