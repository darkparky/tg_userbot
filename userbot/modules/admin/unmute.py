from telethon.errors import UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest

from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, NO_SQL, UNMUTE_RIGHTS
from userbot.modules.dbhelper import unmute
from userbot.utils import get_user_from_event


@register(outgoing=True, group_only=True, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):
    """ For .unmute command, unmute the target """
    # Admin or creator check
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    if not is_mongo_alive() or not is_redis_alive():
        await unmot.edit(NO_SQL)
        return
    # If admin or creator, inform the user and start unmuting
    await unmot.edit('```Unmuting...```')
    user = await get_user_from_event(unmot)
    if user:
        pass
    else:
        return

    if await unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit("`Error! User probably already unmuted.`")
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNMUTE_RIGHTS))
            await unmot.edit("```Unmuted Successfully```")
        except UserIdInvalidError:
            await unmot.edit("`Uh oh my unmute logic broke!`")
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                               f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                               f"CHAT: {unmot.chat.title}(`{unmot.chat_id}`)")
