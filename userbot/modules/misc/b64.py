import pybase64

from userbot.events import register


@register(outgoing=True, pattern="^.b64 (en|de)(?:\s+(.*))?")
async def endecrypt(query):
    """ For .b64 command, find the base64 encoding of the given string. """
    reply_message = await query.get_reply_message()
    text = query.pattern_match.group(2) or reply_message.text
    if query.pattern_match.group(1) == "en":
        lething = str(pybase64.b64encode(bytes(text, "utf-8")))[2:]
        await query.reply("Encoded: `" + lething[:-1] + "`")
    else:
        lething = str( pybase64.b64decode(bytes(text, "utf-8"), validate=True))[2:]
        await query.reply("Decoded: `" + lething[:-1] + "`")