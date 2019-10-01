import os

from gtts import gTTS

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.modules.misc import LANG
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """ For .tts command, a wrapper for Google Text-to-Speech. """
    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit("`Give a text or reply to a "
                         "message for Text-to-Speech!`")
        return

    opts, message = parse_arguments(message, ['slow', 'lang'])
    lang = opts.get('lang', LANG)
    slow = opts.get('slow', False)

    try:
        gTTS(message, lang, slow)
    except AssertionError:
        await query.edit('The text is empty.\n'
                         'Nothing left to speak after pre-precessing, '
                         'tokenizing and cleaning.')
        return
    except ValueError:
        await query.edit('Language is not supported.')
        return
    except RuntimeError:
        await query.edit('Error loading the languages dictionary.')
        return

    await query.delete()

    tts = gTTS(message, lang, slow)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, lang, slow)
        tts.save("k.mp3")
    with open("k.mp3", "r"):
        await query.client.send_file(query.chat_id, "k.mp3", voice_note=True, reply_to=textx)
        os.remove("k.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "tts of " + message + " executed successfully!")

add_help_item(
    ".tts",
    "Misc",
    "Uses Google Text to Speech to say the message.",
    """
    `.tts [options] (message)`
    
    Or, in reply to a message
    `.tts [options]`
    
    Options:
    `.slow`: Say the message slowly.
    `.lang`: Message to speak in.
    """
)
