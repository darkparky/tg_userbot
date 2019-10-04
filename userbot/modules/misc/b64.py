import pybase64

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.b64\s+(en|de)(?:\s+(.*))?")
async def endecrypt(query):
    """ For .b64 command, find the base64 encoding of the given string. """
    reply_message = await query.get_reply_message()
    text = query.pattern_match.group(2) or reply_message.text
    if query.pattern_match.group(1) == "en":
        lething = str(pybase64.b64encode(bytes(text, "utf-8")))[2:]
        await query.reply("Encoded: `" + lething[:-1] + "`")
    else:
        lething = str(pybase64.b64decode(bytes(text, "utf-8"), validate=True))[2:]
        await query.reply("Decoded: `" + lething[:-1] + "`")

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