from asyncio.tasks import sleep

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest

from userbot.events import register
from userbot.modules.admin import BANNED_RIGHTS, UNBAN_RIGHTS


@register(outgoing=True, group_only=True, pattern="^.delusers(?: |$)(.*)")
async def rm_deletedacc(show):
    """ For .delusers command, clean deleted accounts. """
    con = show.pattern_match.group(1)
    del_u = 0
    del_status = "`No deleted accounts found, Group is cleaned as Hell`"

    if con != "clean":
        await show.edit("`Searching for zombie accounts...`")
        async for user in show.client.iter_participants(show.chat_id,
                                                        aggressive=True):
            if user.deleted:
                del_u += 1

        if del_u > 0:
            del_status = f"found **{del_u}** \
                deleted account(s) in this group \
            \nclean them by using .delusers clean"

        await show.edit(del_status)
        return

    # Here laying the sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.edit("`You aren't an admin here!`")
        return

    await show.edit("`Cleaning deleted accounts...`")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.edit("`You don't have enough rights.`")
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
            await sleep(1)
    if del_u > 0:
        del_status = f"cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"cleaned **{del_u}** deleted account(s) \
\n**{del_a}** deleted admin accounts are not removed"

    await show.edit(del_status)