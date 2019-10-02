from ..help import add_help_item
from userbot.events import register
from userbot.utils import list_admins, make_mention


@register(outgoing=True, pattern="^.admins?")
async def notif_admins(msg):
    mentions = map(make_mention, await list_admins(msg))
    response = ' '.join(mentions)

    reply_message = await msg.get_reply_message()

    await msg.client.send_message(msg.chat, response, reply_to=reply_message)
    await msg.delete()

add_help_item(
    ".admins",
    "Misc",
    "Mention all admins (besides bots) in the current chat.",
    """
    `.admins`
    """
)