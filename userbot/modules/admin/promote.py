from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, NO_PERM
from userbot.utils import get_user_from_event


@register(outgoing=True, group_only=True, pattern=r"^\.promote(?: |$)(.*)")
async def promote(promt):
    """ For .promote command, do promote targeted person """
    # Get targeted chat
    chat = await promt.get_chat()
    # Grab admin status or creator in a chat
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, also return
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=True,
                                 invite_users=True,
                                 change_info=True,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit("Promoting...")

    user = await get_user_from_event(promt)
    if user:
        pass
    else:
        return

    # Try to promote if current user is admin or creator
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, "Admin"))
        await promt.edit("`Promoted Successfully!`")

    # If Telethon spit BadRequestError, assume
    # we don't have Promote permission
    except BadRequestError:
        await promt.edit(NO_PERM)
        return

    # Announce to the logging group if we have promoted successfully
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#PROMOTE\n"
                           f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {promt.chat.title}(`{promt.chat_id}`)")


add_help_item(
    ".promote",
    "Admin",
    "Promote the selected user.",
    """
    `.promote (username|userid)`

    Or, in reply to a user
    `.promote`
    """
)
