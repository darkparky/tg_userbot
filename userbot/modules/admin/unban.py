from telethon.errors import UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, UNBAN_RIGHTS
from userbot.utils import get_user_from_event


@register(outgoing=True, group_only=True, pattern=r"^\.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ For .unban command, unban the target """
    # Here laying the sanity check
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    # If everything goes well...
    await unbon.edit("`Unbanning...`")

    user_full = await get_user_from_event(unbon)
    if not user_full:
        return

    user = user_full.user

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit("```Unbanned Successfully```")

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                               f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                               f"CHAT: {unbon.chat.title}(`{unbon.chat_id}`)")
    except UserIdInvalidError:
        await unbon.edit("`Uh oh my unban logic broke!`")


add_help_item(
    ".unban",
    "Admin",
    "Unban the selected user.",
    """
    `.unban (username|userid)`

    Or, in reply to a user
    `.unban`
    """
)
