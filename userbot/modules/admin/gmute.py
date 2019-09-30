from userbot import is_mongo_alive, is_redis_alive, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.admin import NO_SQL
from userbot.modules.dbhelper import gmute
from userbot.utils import get_user_from_event


@register(outgoing=True, group_only=True, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """ For .gmute command, gmutes the target in the userbot """
    # Admin or creator check
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Check if the function running under SQL mode
    if not is_mongo_alive() or not is_redis_alive():
        await gspdr.edit(NO_SQL)
        return
    user = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    # If pass, inform and start gmuting
    await gspdr.edit("`Grabs a huge, sticky duct tape!`")

    if await gmute(user.id) is False:
        await gspdr.edit('`Error! User probably already gmuted.`')
    else:
        await gspdr.edit("`Globally taped!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")