from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.save$")
async def save_message(e):
    reply_message = await e.get_reply_message()
    if not reply_message:
        await e.edit("Give me something to save", delete_in=3)
        return

    await e.delete()
    me = await e.client.get_me()
    await reply_message.forward_to(me)


add_help_item(
    ".save",
    "Utils",
    "Save a message by forwarding it to yourself.",
    """
    In reply to the message you want to save
    `.save`
    """
)
