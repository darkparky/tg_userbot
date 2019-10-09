import random
import re

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.scramble(\s+[\S\s]+|$)")
async def scramble_message(e):
    reply_message = await e.get_reply_message()
    text = e.pattern_match.group(1) or reply_message.text
    words = re.split(r"\s", text)
    scrambled = map(scramble_word, words)
    text = ' '.join(scrambled)
    await e.edit(text)


def scramble_word(word):
    if len(word) < 4:
        return word

    first_letter = word[0]
    last_letter = word[-1]
    middle_letters = list(word[1:-1])
    random.shuffle(middle_letters)

    return first_letter + ''.join(middle_letters) + last_letter


add_help_item(
    ".scramble",
    "Fun",
    "Scrambles a message in a way that the human "
    "brain can still understand.",
    """
    `.scramble (message)`
    
    Or, in reply to a message
    `.scramble`
    """
)
