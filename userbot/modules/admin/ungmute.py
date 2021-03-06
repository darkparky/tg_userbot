from ..help import add_help_item
from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_SQL
from userbot.modules.dbhelper import ungmute
from userbot.utils import get_user_from_event


@register(outgoing=True, group_only=True, pattern=r"^\.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    """ For .ungmute command, ungmutes the target in the userbot """
    # Admin or creator check
    chat = await un_gmute.get_chat()

    # Check if the function running under SQL mode
    if not is_mongo_alive() or not is_redis_alive():
        await un_gmute.edit(NO_SQL)
        return

    user_full = await get_user_from_event(un_gmute)
    if not user_full:
        return

    user = user_full.user

    # If pass, inform and start ungmuting
    await un_gmute.edit('```Ungmuting...```')

    if await ungmute(user.id) is False:
        await un_gmute.edit("`Error! User probably not gmuted.`")
    else:

        # Inform about success
        await un_gmute.edit("```Ungmuted Successfully```")

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#UNGMUTE\n"
                               f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                               f"CHAT: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


add_help_item(
    ".ungmute",
    "Admin",
    "Stop globally muting a user.",
    """
    `.ungmute (username|userid)`

    Or, in reply to a user
    `.ungmute`
    """
)
