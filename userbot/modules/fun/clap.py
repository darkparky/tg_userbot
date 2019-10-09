import unicodedata
import string

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.clap(\s+[\S\s]+|$)")
async def clappify(e):
    reply_message = await e.get_reply_message()
    text = e.pattern_match.group(1) or reply_message.text
    clapped = ' '.join([f"{word} 👏" for word in text.split(' ')])
    await e.edit(clapped)


add_help_item(
    ".clap",
    "Fun",
    "Do some unicode voodoo to flip a message upside down.",
    """
    `.flip (message)`
    
    Or, in reply to a message
    `.flip`
    """
)
