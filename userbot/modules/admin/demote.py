from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, NO_PERM
from userbot.utils import get_user_from_event


@register(group_only=True, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    """ For .demote command, do demote targeted person """
    # Admin right check
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    # If passing, declare that we're going to demote
    await dmod.edit("`Demoting...`")

    user = await get_user_from_event(dmod)
    if user:
        pass
    else:
        return

    # New rights after demotion
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    # Edit Admin Permission
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, "Admin"))

    # If we catch BadRequestError from Telethon
    # Assume we don't have permission to demote
    except BadRequestError:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit("`Demoted Successfully!`")

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#DEMOTE\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {dmod.chat.title}(`{dmod.chat_id}`)")