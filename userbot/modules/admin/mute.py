from telethon.errors import (UserIdInvalidError, UserAdminInvalidError,
                             ChatAdminRequiredError, BadRequestError)
from telethon.tl.functions.channels import EditBannedRequest

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID, is_mongo_alive, is_redis_alive
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, NO_SQL, MUTE_RIGHTS
from userbot.modules.dbhelper import mute
from userbot.utils import get_user_from_event


@register(outgoing=True, group_only=True, pattern=r"^\.mute(?: |$)(.*)")
async def spider(spdr):
    """
    This function is basically muting peeps
    """
    # Check if the function running under SQL mode
    if not is_mongo_alive() or not is_redis_alive():
        await spdr.edit(NO_SQL)
        return

    # Admin or creator check
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit("`Mute Error! You are not supposed to mute yourself!`")
        return

    # If everything goes well, do announcing and mute
    await spdr.edit("`Gets a tape!`")
    if await mute(spdr.chat_id, user.id) is False:
        return await spdr.edit('`Error! User probably already muted.`')
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))
            # Announce that the function is done
            await spdr.edit("`Safely taped!`")

            # Announce to logging group
            if BOTLOG:
                await spdr.client.send_message(
                    BOTLOG_CHATID, "#MUTE\n"
                                   f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                                   f"CHAT: {spdr.chat.title}(`{spdr.chat_id}`)")
        except UserIdInvalidError:
            return await spdr.edit("`Uh oh my unmute logic broke!`")

        # These indicate we couldn't hit him an API mute, possibly an
        # admin?

        except (UserAdminInvalidError, ChatAdminRequiredError,
                BadRequestError):
            return await spdr.edit("""`I couldn't mute on the API,
            could be an admin possibly?
            Anyways muted on the userbot.
            I'll automatically delete messages
            in this chat from this person`""")


add_help_item(
    ".mute",
    "Admin",
    "Mute a user in the current chat.",
    """
    `.mute (username|userid)`
    
    Or, in reply to a user
    `.mute`
    """
)
