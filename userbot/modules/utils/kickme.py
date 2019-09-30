from telethon.tl.functions.channels import LeaveChannelRequest

from userbot import bot
from userbot.events import register


@register(outgoing=True, pattern="^.kickme$")
async def kickme(leave):
    """ Basically it's .kickme command """
    await leave.edit("`Nope, no, no, I go away`")
    await bot(LeaveChannelRequest(leave.chat_id))