import io
import os

from google.cloud.speech_v1 import types
from google.cloud.speech_v1.gapic import enums

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID, STTClient, stt, bot
from userbot.events import register
from userbot.utils import parse_arguments

DEFAULT_LANG = "en-US"


@register(outgoing=True, pattern=r"^\.stt(\s+[\s\S]+|$)")
async def speech_to_text(e):
    opts = e.pattern_match.group(1) or ""
    args, _ = parse_arguments(opts, ['lang'])

    lang = args.get('lang', DEFAULT_LANG)
    await e.edit("**Transcribing...**")

    message = await e.get_reply_message()
    file = message.audio or message.voice

    if not file:
        await e.edit("**No audio file specified**", delete_in=3)
        return

    file = await bot.download_file(file)

    content = io.BytesIO(file)
    audio = types.RecognitionAudio(content=file)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.OGG_OPUS,
        sample_rate_hertz=16000,
        language_code=lang
    )

    response = STTClient.long_running_recognize(config, audio)
    op_result = response.result()
    result = op_result.results[0].alternatives[0]

    output = f"**Transcript:** {result.transcript}\n\n**Confidence:** __{round(result.confidence, 5)}__"
    await e.edit(output)


add_help_item(
    ".stt",
    "Misc",
    "Uses google speech to text to transcribe an audio message.",
    """
    In reply to a message containing audio
    `.stt [options]`
    
    **Options:**
    `lang`: Language code of the message.
    """
)
