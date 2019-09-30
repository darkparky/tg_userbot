from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditBannedRequest

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_ADMIN, NO_PERM, BANNED_RIGHTS
from userbot.utils import get_user_from_event


@register(group_only=True, pattern="^.ban(?: |$)(.*)")
async def ban(bon):
    """ For .ban command, do a ban at targeted person """
    # Here laying the sanity check
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    # Announce that we're going to whack the pest
    await bon.edit("`Whacking the pest!`")

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except BadRequestError:
        await bon.edit(NO_PERM)
        return
    # Helps ban group join spammers more easily
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        bmsg = "`I dont have enough rights! But still he was banned!`"
        await bon.edit(bmsg)
        return
    # Delete message and then tell that the command
    # is done gracefully
    # Shout out the ID, so that fedadmins can fban later

    await bon.edit("`{}` was banned!".format(str(user.id)))

    # Announce to the logging group if we have demoted successfully
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {bon.chat.title}(`{bon.chat_id}`)")