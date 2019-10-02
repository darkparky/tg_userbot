from ..help import add_help_item
from userbot.events import register

IMAGE_FILE = "userbot/images/banhammer.mp4"


@register(pattern=r"^!!hammer(.*|$)")
async def no_screenshots(e):
    reply_message = await e.get_reply_message()
    await e.delete()
    await e.client.send_file(
        e.chat_id,
        IMAGE_FILE,
        reply_to=reply_message)


add_help_item(
    "!!hammer",
    "Meta",
    "Show a ban hammer video.",
    "`!!hammer`"
)
