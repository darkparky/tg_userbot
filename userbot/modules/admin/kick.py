from asyncio.tasks import sleep

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, NO_PERM
from userbot.utils import get_user_from_event


@register(outgoing=True, group_only=True, pattern=r"^\.kick(?: |$)(.*)")
async def kick(usr):
    """ For .kick command, kick someone from the group using the userbot. """
    # Admin or creator check
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user_full = await get_user_from_event(usr)
    if not user_full:
        return

    user = user_full.user

    await usr.edit("`Kicking...`")

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except:
        await usr.edit(NO_PERM)
        return

    kmsg = "`Kicked` [{}](tg://user?id={})`!`"
    await usr.edit(kmsg.format(user.first_name, user.id))

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
                           f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                           f"CHAT: {usr.chat.title}(`{usr.chat_id}`)\n")


add_help_item(
    ".kick",
    "Admin",
    "Kicks (not bans) a user from the current group.",
    """
    `.kick (username|userid)`
    
    Or, in reply to a user
    `.kick`
    """
)
