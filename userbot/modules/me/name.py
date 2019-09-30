from telethon.tl.functions.account import UpdateProfileRequest

from userbot import bot
from userbot.events import register

NAME_OK = "```Your name was successfully changed.```"


@register(outgoing=True, pattern="^.name")
async def update_name(name):
    """ For .name command, change your name in Telegram. """
    newname = name.text[6:]
    if " " not in newname:
        firstname = newname
        lastname = ""
    else:
        namesplit = newname.split(" ", 1)
        firstname = namesplit[0]
        lastname = namesplit[1]

    await bot(UpdateProfileRequest(first_name=firstname, last_name=lastname))
    await name.edit(NAME_OK)