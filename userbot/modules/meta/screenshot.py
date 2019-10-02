from ..help import add_help_item
from userbot.events import register

IMAGE_FILE = "userbot/images/screenshot.jpg"
DEFAULT_MESSAGE = ("Do **not** take screenshots of code or errors. "
                   "If you want to share code, please use one of the "
                   "many pastebins available, such as del.dog, hasteb.in, "
                   "dpaste.de, codepile.net, or pastebin.com.")


@register(pattern=r"^!!screenshot(.*|$)")
async def no_screenshots(e):
    reply_message = await e.get_reply_message()
    message = e.pattern_match.group(1) or DEFAULT_MESSAGE
    await e.delete()
    await e.client.send_file(
        e.chat_id,
        IMAGE_FILE,
        caption=message,
        reply_to=reply_message)


add_help_item(
    "!!screenshot",
    "Meta",
    "Warn idiots about taking screenshots of code.",
    "`!!screenshot`"
)
