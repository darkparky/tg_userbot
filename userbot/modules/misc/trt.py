from emoji import get_emoji_regexp
# noinspection PyProtectedMember
from googletrans import Translator, LANGUAGES

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.utils import parse_arguments
from . import LANG


@register(outgoing=True, pattern=r"^\.trt(\s+[\s\S]+|$)")
async def translateme(trans):
    """ For .trt command, translate the given text using Google Translate. """
    translator = Translator()
    textx = await trans.get_reply_message()
    message = trans.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await trans.edit("`Give a text or reply "
                         "to a message to translate!`")
        return

    opts, message = parse_arguments(message, ['to', 'from'])
    dest_lang = opts.get('to', LANG)
    src_lang = opts.get('from', 'auto')

    trans.edit("Translating...")
    try:
        reply_text = translator.translate(deEmojify(message), dest=dest_lang, src=src_lang)
    except ValueError:
        await trans.edit("Invalid destination language.")
        return

    source_lan = LANGUAGES[f'{reply_text.src.lower()}']
    transl_lan = LANGUAGES[f'{reply_text.dest.lower()}']
    reply_text = f"**Source ({source_lan.title()}):**`\n{message}`**\n\
\nTranslation ({transl_lan.title()}):**`\n{reply_text.text}`"

    await trans.client.send_message(trans.chat_id, reply_text)
    await trans.delete()
    if BOTLOG:
        await trans.client.send_message(
            BOTLOG_CHATID,
            f"Translate query {message} was executed successfully",
        )


def deEmojify(inputString):
    """ Remove emojis and other non-safe characters from string """
    return get_emoji_regexp().sub(u'', inputString)

add_help_item(
    ".trt",
    "Misc",
    "Uses Google Translate to translate the supplied string.",
    """
    `.trt [options] (message)`
    
    Options:
    `.to`: To language code
    `.from`: From language code
    """
)
