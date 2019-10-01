from telethon.tl.functions.channels import LeaveChannelRequest

from ..help import add_help_item
from userbot import bot
from userbot.events import register


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ Basically it's .kickme command """
    await leave.edit("`Nope, no, no, I go away`")
    await bot(LeaveChannelRequest(leave.chat_id))

add_help_item(
    ".kickme",
    "Utilities",
    "Kick yourself from the current chat.",
    """
    In that chat you want to be kicked from
    `.kickme`
    """
)