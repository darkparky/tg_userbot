from ..help import add_help_item

from userbot.events import register

NO_META = """Please don't ask meta questions like:

"Any user of $x here?"
"Anyone used technology $y?"
"Hello I need help on $z"

Just ask about your problem directly! With 42k+ people the probability that someone will help is pretty high.
Also please read: http://catb.org/~esr/faqs/smart-questions.html"""

@register(pattern="^!!meta")
async def meta_interjection(e):
    reply_message = await e.get_reply_message()
    await e.respond(NO_META, reply_to=reply_message)
    await e.delete()

add_help_item(
    "!!meta",
    "Meta",
    "Warn users about asking meta questions.",
    "`!!meta`"
)
