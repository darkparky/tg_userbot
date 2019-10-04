import os

from moviepy import editor as mp
from pytube import YouTube
from pytube.helpers import safe_filename

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.ytmp3 (\S*)")
async def youtube_mp3(yt):
    reply_message = await yt.get_reply_message()
    url = yt.pattern_match.group(1)

    await yt.edit("**Processing...**")

    video = YouTube(url)
    stream = video.streams.filter(progressive=True,
                                  subtype="mp4").first()

    await yt.edit("**Downloading video...**")
    stream.download(filename='video')

    await yt.edit("**Converting video...**")
    clip = mp.VideoFileClip('video.mp4')
    clip.audio.write_audiofile(f'{safe_filename(video.title)}.mp3')

    await yt.edit("**Sending mp3...**")
    await yt.client.send_file(yt.chat.id,
                              f'{safe_filename(video.title)}.mp3',
                              caption=f"{video.title}",
                              reply_to=reply_message)

    await yt.delete()

    os.remove('video.mp4')
    os.remove(f'{safe_filename(video.title)}.mp3')


add_help_item(
    ".ytmp3",
    "Misc",
    "Convert a YouTube video to a mp3 and send it.",
    """
    `.ytmp3 (url)`
    """
)
