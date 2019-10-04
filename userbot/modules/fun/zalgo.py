import random

from ..help import add_help_item
from userbot import ZALG_LIST
from userbot.events import register


@register(outgoing=True, pattern=r"^\.zal(?:go)?(?: |$)(.*)")
async def zal(zgfy):
    """ Invoke the feeling of chaos. """
    reply_text = list()
    textx = await zgfy.get_reply_message()
    message = zgfy.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await zgfy.edit(
            "`gͫ ̆ i̛ ̺ v͇̆ ȅͅ   a̢ͦ   s̴̪ c̸̢ ä̸ rͩͣ y͖͞   t̨͚ é̠ x̢͖  t͔͛`"
        )
        return

    for charac in message:
        if not charac.isalpha():
            reply_text.append(charac)
            continue

        for _ in range(0, 3):
            randint = random.randint(0, 2)

            if randint == 0:
                charac = charac.strip() + \
                         random.choice(ZALG_LIST[0]).strip()
            elif randint == 1:
                charac = charac.strip() + \
                         random.choice(ZALG_LIST[1]).strip()
            else:
                charac = charac.strip() + \
                         random.choice(ZALG_LIST[2]).strip()

        reply_text.append(charac)

    await zgfy.edit("".join(reply_text))


add_help_item(
    ".zal",
    "Fun",
    "Z̥̯a̧̖l̹͘g̵̞ò̜f̶͕y̐ͅ aͩ͞ m̩͛e͔ͧs͙͠ṡ̶a̭ͅg̶ ̾ē̸",
    """
    `.zal (message)`
    
    Or, in reply to a message
    `.zal`
    """
)
