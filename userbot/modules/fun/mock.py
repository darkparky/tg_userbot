import random

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.mock(?: |$)(.*)")
async def spongemocktext(mock):
    """ Do it and find the real fun. """
    reply_text = list()
    textx = await mock.get_reply_message()
    message = mock.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await mock.edit("`gIvE sOMEtHInG tO MoCk!`")
        return

    for charac in message:
        if charac.isalpha() and random.randint(0, 1):
            to_app = charac.upper() if charac.islower() else charac.lower()
            reply_text.append(to_app)
        else:
            reply_text.append(charac)

    await mock.edit("".join(reply_text))

add_help_item(
    ".mock",
    "Fun",
    "Mocks the selected text like the [spongebob meme](https://knowyourmeme.com/memes/mocking-spongebob).",
    """
    `.mock (message)`
    
    Or, in reply to a message
    `.mock`
    """
)
