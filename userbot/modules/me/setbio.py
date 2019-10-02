from telethon.tl.functions.account import UpdateProfileRequest

from ..help import add_help_item
from userbot import bot
from userbot.events import register

BIO_SUCCESS = "```Successfully edited Bio.```"


@register(outgoing=True, pattern="^.setbio (.*)")
async def set_biograph(setbio):
    """ For .setbio command, set a new bio for your profile in Telegram. """
    newbio = setbio.pattern_match.group(1)
    await bot(UpdateProfileRequest(about=newbio))
    await setbio.edit(BIO_SUCCESS)


add_help_item(
    ".setbio",
    "Me",
    "Set your bio.",
    """
    `.setbio (content)`
    """
)
