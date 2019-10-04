import random
import re

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.str(?:etch)?(?: |$)(.*)")
async def stretch(stret):
    """ Stretch it."""
    textx = await stret.get_reply_message()
    message = stret.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await stret.edit("`GiiiiiiiB sooooooomeeeeeee teeeeeeext!`")
        return

    count = random.randint(3, 10)
    reply_text = re.sub(r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵаеиоуюяыэё])", (r"\1" * count),
                        message)
    await stret.edit(reply_text)


add_help_item(
    ".str",
    "Fun",
    "Stretches vowels in a message.",
    """
    `.str (message)`
    
    Or, in reply to a message
    `.str`
    """
)
