from asyncio.tasks import sleep

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl.functions.channels import EditBannedRequest

from ..help import add_help_item
from userbot.events import register
from userbot.modules.admin import BANNED_RIGHTS, UNBAN_RIGHTS


@register(outgoing=True, group_only=True, pattern="^.clean(?: |$)(.*)")
async def rm_deletedacc(show):
    """ For .clean command, clean deleted accounts. """
    con = show.pattern_match.group(1)
    del_u = 0
    del_status = "**No deleted accounts found**"

    # Sanity check
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Well
    if not admin and not creator:
        await show.edit("You aren't an admin here!", delete_in=3)
        return

    await show.edit("**Cleaning deleted accounts...**")
    del_u = 0
    del_a = 0

    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client(
                    EditBannedRequest(show.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await show.edit("You don't have sufficient permissions", delete_in=3)
                return
            except UserAdminInvalidError:
                del_u -= 1
                del_a += 1
            await show.client(
                EditBannedRequest(show.chat_id, user.id, UNBAN_RIGHTS))
            del_u += 1
            await sleep(1)
    if del_u > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s)"

    if del_a > 0:
        del_status = f"Cleaned **{del_u}** deleted account(s) \n"
        del_status += f"**{del_a}** deleted admin accounts were not removed"

    await show.edit(del_status)


add_help_item(
    ".clean",
    "Admin",
    "Clean the current chat of deleted accounts.",
    """
    `.clean`
    """
)
