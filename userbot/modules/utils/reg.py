""" Allows !! commands to be registered """

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^.reg([\S\s]+|$)")
async def register_command(e):
    reply_message = e.get_reply_message()
    params = e.pattern_match.group(1)

