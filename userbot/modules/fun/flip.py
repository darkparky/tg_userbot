import unicodedata
import string

from ..help import add_help_item
from userbot.events import register


# Define dual character. Make sure that mapping is bijective.
FLIP_RANGES = [
    (string.ascii_lowercase, "ɐqɔpǝɟƃɥᴉɾʞꞁɯuodbɹsʇnʌʍxʎz"),
    # alternatives: l:ʅ
    (string.ascii_uppercase, "ⱯᗺƆᗡƎᖵ⅁HIᒋ⋊ꞀWNOԀꝹᴚS⊥∩ɅMX⅄Z"),
    # alternatives: L:ᒣ⅂, J:ſ, F:߃Ⅎ, A:∀ᗄ, U:Ⴖ, W:Ϻ, C:ϽↃ, Q:Ό, M:Ɯꟽ
    (string.digits, "0ІᘔƐᔭ59Ɫ86"),
    (string.punctuation, "¡„#$%⅋,)(*+'-˙/:؛>=<¿@]\\[ᵥ‾`}|{~"),
]

UNICODE_COMBINING_DIACRITICS = {'̈': '̤', '̊': '̥', '́': '̗', '̀': '̖',
                                '̇': '̣', '̃': '̰', '̄': '̱', '̂': '̬', '̆': '̯', '̌': '̭',
                                '̑': '̮', '̍': '̩'}

TRANSLITERATIONS = {'ß': 'ss'}

# character lookup
_CHARLOOKUP = {}
for chars, flipped in FLIP_RANGES:
    _CHARLOOKUP.update(zip(chars, flipped))

# get reverse direction
for char in _CHARLOOKUP.copy():
    # make 1:1 back transformation possible
    assert (_CHARLOOKUP[char] not in _CHARLOOKUP
            or _CHARLOOKUP[_CHARLOOKUP[char]] == char), \
        ("%s has ambiguous mapping" % _CHARLOOKUP[char])
    _CHARLOOKUP[_CHARLOOKUP[char]] = char

# lookup for diacritical marks, reverse first
_DIACRITICSLOOKUP = dict([(UNICODE_COMBINING_DIACRITICS[char], char)
                          for char in UNICODE_COMBINING_DIACRITICS])
_DIACRITICSLOOKUP.update(UNICODE_COMBINING_DIACRITICS)


def transform(text, transliterations=None):
    transliterations = transliterations or TRANSLITERATIONS

    for character in transliterations:
        text = text.replace(character, transliterations[character])

    input_chars = list(text)
    input_chars.reverse()

    output = []
    for character in input_chars:
        if character in _CHARLOOKUP:
            output.append(_CHARLOOKUP[character])
        else:
            char_normalized = unicodedata.normalize("NFD", character)

            for c in char_normalized[:]:
                if c in _CHARLOOKUP:
                    char_normalized = char_normalized.replace(c, _CHARLOOKUP[c])
                elif c in _DIACRITICSLOOKUP:
                    char_normalized = char_normalized.replace(c, _DIACRITICSLOOKUP[c])

            output.append(unicodedata.normalize("NFC", char_normalized))

    return ''.join(output)


@register(outgoing=True, pattern=r"^\.flip([\S\s]+|$)")
async def flip_message(e):
    reply_message = await e.get_reply_message()
    text = e.pattern_match.group(1) or reply_message.text
    flipped = transform(text)
    await e.edit(flipped)


add_help_item(
    ".flip",
    "Fun",
    "Do some unicode voodoo to flip a message upside down.",
    """
    `.flip (message)`
    
    Or, in reply to a message
    `.flip`
    """
)
