import pybase64

from ..help import add_help_item
from userbot.events import register
from userbot.utils.tgdoc import *


@register(outgoing=True, pattern=r"^\.b64\s+(en|de)(?:\s+(.*))?")
async def endecrypt(e):
    """ For .b64 command, find the base64 encoding of the given string. """
    reply_message = await e.get_reply_message()
    text = e.pattern_match.group(2) or reply_message.message
    output = Section(SubSection(Bold("Input"), Code(text), indent=0), indent=0)
    if e.pattern_match.group(1) == "en":
        lething = str(pybase64.b64encode(bytes(text, "utf-8")))[2:]
        output += SubSection(Bold("Encoded"), Code(lething[:-1]), indent=0)
    else:
        lething = str(pybase64.b64decode(bytes(text, "utf-8"), validate=True))[2:]
        output += SubSection(Bold("Decoded"), Code(lething[:-1]), indent=0)
    await e.edit(str(output))


add_help_item(
    ".b64",
    "Misc",
    "Base64 encode/decode the message or replied to message.",
    """
    `.b64 (en|de) (message)`
    
    Or, in reply to a message
    `.b64 (en|de)`
    """
)