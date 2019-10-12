from ..help import add_help_item
from userbot.events import register
from userbot.utils.tgdoc import *

SMALL_CAPS = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘqʀꜱᴛᴜᴠᴡxʏᴢ"
)


@register(outgoing=True, pattern=r"\.smol(\s+[\S\s]+|$)")
async def make_smol(e):
    reply_message = await e.get_reply_message()
    text = e.pattern_match.group(1) or reply_message.text
    smol = text.translate(SMALL_CAPS)
    await e.edit(smol)
