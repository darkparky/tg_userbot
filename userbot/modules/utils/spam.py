from telethon.tl.functions.users import GetFullUserRequest

from userbot.modules.utils.user import fetch_info
from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register

SPAMWATCH_CHAT_ID = 1312712379


@register(outgoing=True, pattern=r"^\.spam$")
async def forward_to_spamwatch(e):
    reply_message = await e.get_reply_message()
    if not reply_message:
        await e.edit("**Please select a message**", delete_in=3)

    await e.edit("**Flagging spam...**")

    forwarded = await reply_message.forward_to(SPAMWATCH_CHAT_ID)
    replied_user = await e.client(GetFullUserRequest(reply_message.from_id))
    user_info = await fetch_info(replied_user, mention=True)

    await forwarded.reply(user_info)
    await e.edit("**Flagged as spam**", delete_in=3)

add_help_item(
    ".spam",
    "Utilities",
    "Flag a message as spam by forwarding it to "
    "@SpamWatchSupport. Be careful with this, as "
    "it can lead to your account getting limited. "
    "If that happens message @SpamBot and tell it "
    "that you're a memeber of Spam Watch.",
    """
    In reply to the message you want to flag
    `.spam`
    """
)
