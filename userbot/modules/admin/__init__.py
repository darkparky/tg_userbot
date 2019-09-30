from telethon.errors import UserAdminInvalidError, ChatAdminRequiredError, BadRequestError, UserIdInvalidError
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from userbot import is_mongo_alive, is_redis_alive, CMD_HELP
from userbot.events import register
from userbot.modules.dbhelper import get_muted, get_gmuted

PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing image`"
NO_ADMIN = "`You aren't an admin!`"
NO_PERM = "`You don't have sufficient permissions!`"
NO_SQL = "`Database connections failing!`"

CHAT_PP_CHANGED = "`Chat Picture Changed`"
CHAT_PP_ERROR = "`Some issue with updating the pic,`" \
                "`maybe you aren't an admin,`" \
                "`or don't have the desired rights.`"
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

KICK_RIGHTS = ChatBannedRights(until_date=None, view_messages=True)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

@register(incoming=True, disable_errors=True)
async def muter(moot):
    """ Used for deleting the messages of muted people """
    if not is_mongo_alive() or not is_redis_alive():
        return
    muted = await get_muted(moot.chat_id)
    gmuted = await get_gmuted()
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if i == moot.sender_id:
                await moot.delete()
                try:
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id,
                                          rights))

                # We couldn't hit him an API mute, probably an admin?
                # Telethon sometimes fails to grab user details properly gaurd
                # it also
                except (UserAdminInvalidError, ChatAdminRequiredError,
                        BadRequestError, UserIdInvalidError):
                    pass
    for i in gmuted:
        if i == moot.sender_id:
            await moot.delete()

CMD_HELP.update({
    "Admin": {
        "promote": "Usage: Reply to message with .promote to promote them.",
        "ban": "Usage: Reply to message with .ban to ban them.",
        "demote":
            "Usage: Reply to message with"
            ".demote to revoke their admin permissions.",
        "unban":
            "Usage: Reply to message with .unban to unban them in this chat.",
        "mute":
            "Usage: Reply tomessage with .mute "
            "to mute them, works on admins too",
        "unmute":
            "Usage: Reply to message with .unmute "
            "to remove them from muted list.",
        "gmute":
            "Usage: Reply to message with .gmute to mute them in all "
            "groups you have in common with them.",
        "ungmute":
            "Usage: Reply message with .ungmute "
            "to remove them from the gmuted list.",
        "delusers": "Usage: Searches for deleted accounts in a group.",
        "delusers clean":
            "Usage: Searches and removes "
            "deleted accounts from the group"
    }
})