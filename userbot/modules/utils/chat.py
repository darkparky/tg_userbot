from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern="^.chat$")
async def chatidgetter(chat):
    """ For .chatid, returns the ID of the chat you are in at that moment. """
    await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")

add_help_item(
    ".chat",
    "Utilities",
    "Returns the ID of the current chat.",
    """
    In the chat you want the ID of
    `.chat`
    """
)
