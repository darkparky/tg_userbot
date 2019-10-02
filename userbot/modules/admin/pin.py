from telethon.errors import BadRequestError
from telethon.tl.functions.messages import UpdatePinnedMessageRequest

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, NO_PERM
from userbot.utils import get_user_from_id


@register(group_only=True, pattern="^.pin(?: |$)(.*)")
async def pin(msg):
    # Admin or creator check
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit("`Reply to a message which you want to pin.`")
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(
            UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await msg.edit(NO_PERM)
        return

    await msg.edit("`Pinned Successfully!`")

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
                           f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {msg.chat.title}(`{msg.chat_id}`)\n"
                           f"LOUD: {not is_silent}")


add_help_item(
    ".pin",
    "Admin",
    "Pin a message in the current group.",
    """
    In reply to a the message you want to pin
    `.pin`
    """
)
