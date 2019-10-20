from spamwatch.errors import UnauthorizedError

from .score import gather_profile_pic_hashes
from ...help import add_help_item
from userbot import spamwatch, bot
from userbot.events import register
from userbot.modules.dbhelper import (add_file_hash)
from userbot.utils import get_user_from_event, parse_arguments, make_mention

CLASSIFYING_MESSAGE = "**Classifying as spam.** {}"


@register(outgoing=True, pattern=r"^\.s(?:pam)?b(?:lock)? flag(\s+[\S\s]+|$)")
async def spamscan_classify(e):
    """ Feed the algorithm by classifying a user either
    as spam or ham """
    args, user = parse_arguments(e.pattern_match.group(1), ['forward', 'reason'])

    reason = args.get('reason', 'spam[gban]')
    args['forward'] = args.get('forward', True)
    args['user'] = user

    await e.edit(CLASSIFYING_MESSAGE.format("**Fetching user information.**"))
    replied_user = await get_user_from_event(e, **args)
    if not replied_user:
        await e.edit("**Failed to get information for user**", delete_in=3)
        return

    me = await bot.get_me()
    if replied_user.user == me:
        await e.edit("**Can't flag yourself as spam**", delete_in=3)
        return

    hashes = await gather_profile_pic_hashes(e, replied_user.user)
    if hashes:
        await e.edit(CLASSIFYING_MESSAGE.format("**Adding profile pic hashes to DB**"))
        for hsh in hashes:
            await add_file_hash(hsh, 'profile pic')

    if spamwatch:
        await e.edit(CLASSIFYING_MESSAGE.format("**Checking spamwatch.**"))
        gbanned = spamwatch.get_ban(replied_user.user.id)

        if not gbanned:
            await e.edit(CLASSIFYING_MESSAGE.format("**Adding to SpamWatch.**"))
            try:
                spamwatch.add_ban(replied_user.user.id, reason)
            except UnauthorizedError:
                pass

    await e.edit(f"**Flagged** {make_mention(replied_user.user)} **as spam**\n"
                 f"**Reason:** {reason}")


add_help_item(
    ".spamblock flag",
    "Utilities",
    "Flag the selected user as a spammer. Hashes their profile "
    "photos and adds them to the database and, if you're a "
    "SpamWatch admin, gbans them. If you're not an admin it "
    "forwards the replied to message to SpamWatch.",
    """
    `.spamblock flag [options] (user id|username)`
    
    Or, in reply to a message
    `.spamblock flag [options]`
    
    **Options:**
    `.forward`: Follow forwarded message
    
    `reason`: The reason for flagging
    """
)
