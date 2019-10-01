from datetime import datetime

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern="^.ping$")
async def ping(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % duration)

add_help_item(
    ".ping",
    "Misc",
    "Measures how long it takes for Telegram's servers "
    "to respond.",
    """
    `.ping`
    """
)
