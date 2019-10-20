from mutagen.mp3 import MP3
from google.cloud.texttospeech_v1.gapic.enums import SsmlVoiceGender
from telethon.tl.types import DocumentAttributeAudio

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID, TTSClient, tts
from userbot.events import register
from userbot.utils import parse_arguments

DEFAULT_LANG = "en-US"
DEFAULT_VOICE = "en-US-Wavenet-F"
DEFAULT_GENDER = "female"

GENDERS = {
    "male": SsmlVoiceGender.MALE,
    "female": SsmlVoiceGender.FEMALE,
    "neutral": SsmlVoiceGender.NEUTRAL
}


@register(outgoing=True, pattern=r"^\.tts(\s+[\s\S]+|$)")
async def text_to_speech(e):
    """ For .tts command, a wrapper for Google Text-to-Speech. """
    textx = await e.get_reply_message()
    message = e.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await e.edit("`Give a text or reply to a "
                         "message for Text-to-Speech!`")
        return

    opts, message = parse_arguments(message, [
        'slow', 'fast', 'lang', 'gender', 'file'
    ])

    lang = opts.get('lang', DEFAULT_LANG)
    voice = opts.get('voice', DEFAULT_VOICE)
    gender = GENDERS.get(opts.get('gender', "neutral"), SsmlVoiceGender.NEUTRAL)

    if opts.get('slow'):
        speed = 0.5
    elif opts.get('fast'):
        speed = 2.0
    else:
        speed = 1.0

    synthesis_input = tts.types.SynthesisInput(text=message)

    voice = tts.types.VoiceSelectionParams(
        name=voice,
        language_code=lang,
        ssml_gender=gender)

    audio_config = tts.types.AudioConfig(
        audio_encoding=tts.enums.AudioEncoding.MP3,
        speaking_rate=speed)

    try:
        response = TTSClient.synthesize_speech(synthesis_input, voice, audio_config)
    except AssertionError:
        await e.edit('The text is empty.\n'
                         'Nothing left to speak after pre-precessing, '
                         'tokenizing and cleaning.')
        return
    except ValueError as err:
        await e.edit('Language is not supported.')
        return
    except RuntimeError:
        await e.edit('Error loading the languages dictionary.')
        return

    await e.delete()

    with open("k.mp3", "wb") as file:
        file.write(response.audio_content)
        audio = MP3("k.mp3")
        await e.client.send_file(
            e.chat_id,
            "k.mp3",
            reply_to=textx,
            attributes=[DocumentAttributeAudio(
                voice=True,
                waveform=bytes(response.audio_content),
                duration=int(audio.info.length)
            )]
        )

    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID, "tts of `" + message + "` executed successfully!")

add_help_item(
    ".tts",
    "Misc",
    "Uses Google Text to Speech to say the message.",
    """
    `.tts [options] (message)`
    
    Or, in reply to a message
    `.tts [options]`
    
    Options:
    `.slow`: Play at half speed.
    `.fast`: Play at double speed.
    
    `lang`: Language code of the message.
    `gender`: `male`, `female`, or `neutral`.
    `voice`: Any of the supported [voice names](https://cloud.google.com/text-to-speech/docs/voices).
    """
)
