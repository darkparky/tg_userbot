# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing various scrapers. """

import os
import shutil
import imageio
from html import unescape
from urllib.error import HTTPError

import moviepy.editor as mp
from emoji import get_emoji_regexp
from google_images_download import google_images_download
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googletrans import LANGUAGES, Translator
from gtts import gTTS
from pytube import YouTube
from pytube.helpers import safe_filename
from requests import get
from search_engine_parser import GoogleSearch
from urbandict import define
from wikipedia import summary
from wikipedia.exceptions import DisambiguationError, PageError

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, CURRENCY_API,
                     YOUTUBE_API_KEY, bot)
from userbot.events import register
from userbot.utils.helpers import parse_arguments

LANG = "en"


@register(outgoing=True, pattern=r"^.img (.*)")
async def img_sampler(event):
    """ For .img command, search and return images matching the query. """
    await event.edit("Processing query...")

    query = event.pattern_match.group(1)
    opts, query = parse_arguments(query)

    response = google_images_download.googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": opts.get('limit', 3),
        "format": opts.get('format', 'jpg'),
        "no_directory": "no_directory"
    }

    # passing the arguments to the function
    await event.edit("Downloading images...")
    paths = response.download(arguments)
    lst = paths[0][query]

    await event.edit("Sending images...")
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst)
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


@register(outgoing=True, pattern=r"^.google(?: |$)(.*)")
async def gsearch(q_event):
    """ For .google command, do a Google search. """
    reply_message = await q_event.get_reply_message()
    query = q_event.pattern_match.group(1)
    opts, query = parse_arguments(query)

    page = opts.get('page', 1)
    gsearch = GoogleSearch()

    query = query or reply_message.text
    gresults = gsearch.search(query, page)
    
    msg = ""
    limit = opts.get('limit', 5)
    for i in range(limit):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link}) \n"
            msg += f"`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Search Query:**\n`" + query + "`\n\n**Results:**\n" +
                       msg,
                       link_preview=False)
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + query + "` was executed successfully",
        )


@register(outgoing=True, pattern=r"^.wiki (.*)")
async def wiki(wiki_q):
    """ For .google command, fetch content from Wikipedia. """
    match = wiki_q.pattern_match.group(1)
    try:
        summary(match)
    except DisambiguationError as error:
        await wiki_q.edit(f"Disambiguated page found.\n\n{error}")
        return
    except PageError as pageerror:
        await wiki_q.edit(f"Page not found.\n\n{pageerror}")
        return
    result = summary(match)
    if len(result) >= 4096:
        file = open("output.txt", "w+")
        file.write(result)
        file.close()
        await wiki_q.client.send_file(
            wiki_q.chat_id,
            "output.txt",
            reply_to=wiki_q.id,
            caption="`Output too large, sending as file`",
        )
        if os.path.exists("output.txt"):
            os.remove("output.txt")
        return
    await wiki_q.edit("**Search:**\n`" + match + "`\n\n**Result:**\n" + result)
    if BOTLOG:
        await wiki_q.client.send_message(
            BOTLOG_CHATID, f"Wiki query {match} was executed successfully")


@register(outgoing=True, pattern="^.ud (.*)")
async def urban_dict(ud_e):
    """ For .ud command, fetch content from Urban Dictionary. """
    await ud_e.edit("Processing...")
    query = ud_e.pattern_match.group(1)
    try:
        define(query)
    except HTTPError:
        await ud_e.edit(f"Sorry, couldn't find any results for: {query}")
        return
    mean = define(query)
    deflen = sum(len(i) for i in mean[0]["def"])
    exalen = sum(len(i) for i in mean[0]["example"])
    meanlen = deflen + exalen
    if int(meanlen) >= 0:
        if int(meanlen) >= 4096:
            await ud_e.edit("`Output too large, sending as file.`")
            file = open("output.txt", "w+")
            file.write("Text: " + query + "\n\nMeaning: " + mean[0]["def"] +
                       "\n\n" + "Example: \n" + mean[0]["example"])
            file.close()
            await ud_e.client.send_file(
                ud_e.chat_id,
                "output.txt",
                caption="`Output was too large, sent it as a file.`")
            if os.path.exists("output.txt"):
                os.remove("output.txt")
            await ud_e.delete()
            return
        await ud_e.edit("Text: **" + query + "**\n\nMeaning: **" +
                        mean[0]["def"] + "**\n\n" + "Example: \n__" +
                        mean[0]["example"] + "__")
        if BOTLOG:
            await ud_e.client.send_message(
                BOTLOG_CHATID, "ud query " + query + " executed successfully.")
    else:
        await ud_e.edit("No result found for **" + query + "**")


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

    opts, message = parse_arguments(message)
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

@register(outgoing=True, pattern=r"^.trt(?: |$)([\s\S]+)?")
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

    opts, message = parse_arguments(message)
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


@register(pattern="^.lang (.*)", outgoing=True)
async def lang(value):
    """ For .lang command, change the default langauge of userbot scrapers. """
    global LANG
    LANG = value.pattern_match.group(1)
    await value.delete()
    if BOTLOG:
        await value.client.send_message(
            BOTLOG_CHATID, "Default language changed to **" + LANG + "**")


@register(outgoing=True, pattern="^.yt (.*)")
async def yt_search(video_q):
    """ For .yt command, do a YouTube search from Telegram. """
    query = video_q.pattern_match.group(1)
    result = ''
    i = 1

    if not YOUTUBE_API_KEY:
        await video_q.edit("`Error: YouTube API key missing!\
            Add it to environment vars or config.env.`")
        return

    opts, query = parse_arguments(query)
    limit = opts.get('limit', 5)

    await video_q.edit("Processing search query...")

    full_response = youtube_search(query, limit)
    videos_json = full_response[1]

    for video in videos_json:
        result += f"{i}. {unescape(video['snippet']['title'])} \
\nhttps://www.youtube.com/watch?v={video['id']['videoId']}\n"

        i += 1

    reply_text = f"**Search Query:**\n`{query}`\n\n**Result:**\n{result}"

    await video_q.edit(reply_text)


def youtube_search(query,
                   order="relevance",
                   limit=5,
                   token=None,
                   location=None,
                   location_radius=None):
    """ Do a YouTube search. """
    youtube = build('youtube',
                    'v3',
                    developerKey=YOUTUBE_API_KEY,
                    cache_discovery=False)
    search_response = youtube.search().list(
        q=query,
        type="video",
        pageToken=token,
        order=order,
        part="id,snippet",
        maxResults=limit,
        location=location,
        locationRadius=location_radius).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result)
    try:
        nexttok = search_response["nextPageToken"]
        return (nexttok, videos)
    except HttpError:
        nexttok = "last_page"
        return (nexttok, videos)
    except KeyError:
        nexttok = "KeyError, try again."
        return (nexttok, videos)


@register(outgoing=True, pattern=r"^.ytdl (.*)")
async def download_video(v_url):
    """ For .ytdl command, download videos from YouTube. """
    query = v_url.pattern_match.group(1)
    opts, url = parse_arguments(query)
    quality = opts.get('res', None)

    await v_url.edit("**Fetching...**")

    video = YouTube(url)

    if quality:
        video_stream = video.streams.filter(progressive=True,
                                            subtype="mp4",
                                            res=quality).first()
    else:
        video_stream = video.streams.filter(progressive=True,
                                            subtype="mp4").first()

    if video_stream is None:
        all_streams = video.streams.filter(progressive=True,
                                           subtype="mp4").all()
        available_qualities = ""

        for item in all_streams[:-1]:
            available_qualities += f"{item.resolution}, "
        available_qualities += all_streams[-1].resolution

        await v_url.edit("**A stream matching your query wasn't found. "
                         "Try again with different options.\n**"
                         "**Available Qualities:**\n"
                         f"{available_qualities}")
        return

    video_size = video_stream.filesize / 1000000

    if video_size >= 50:
        await v_url.edit(
            ("**File larger than 50MB. Sending the link instead.\n**"
             f"Get the video [here]({video_stream.url})\n\n"
             "**If the video plays instead of downloading, "
             "right click(or long press on touchscreen) and "
             "press 'Save Video As...'(may depend on the browser) "
             "to download the video.**"))
        return

    await v_url.edit("**Downloading...**")

    video_stream.download(filename=video.title)

    url = f"https://img.youtube.com/vi/{video.video_id}/maxresdefault.jpg"
    resp = get(url)
    with open('thumbnail.jpg', 'wb') as file:
        file.write(resp.content)

    await v_url.edit("**Uploading...**")
    await bot.send_file(v_url.chat_id,
                        f'{safe_filename(video.title)}.mp4',
                        caption=f"{video.title}",
                        thumb="thumbnail.jpg")

    os.remove(f"{safe_filename(video.title)}.mp4")
    os.remove('thumbnail.jpg')
    await v_url.delete()

@register(outgoing=True, pattern="^.ytmp3 (\S*)")
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


@register(outgoing=True, pattern=r"^.cr (\S*) ?(\S*) ?(\S*)")
async def currency(cconvert):
    """ For .cr command, convert amount, from, to. """
    amount = cconvert.pattern_match.group(1)
    currency_from = cconvert.pattern_match.group(3).upper()
    currency_to = cconvert.pattern_match.group(2).upper()
    data = get(
        f"https://free.currconv.com/api/v7/convert?apiKey={CURRENCY_API}&q={currency_from}_{currency_to}&compact=ultra"
    ).json()
    result = data[f'{currency_from}_{currency_to}']
    result = float(amount) / float(result)
    result = round(result, 5)
    await cconvert.edit(
        f"{amount} {currency_to} is:\n`{result} {currency_from}`")


def deEmojify(inputString):
    """ Remove emojis and other non-safe characters from string """
    return get_emoji_regexp().sub(u'', inputString)


CMD_HELP.update({
    "Scraping": {
        'img':
            "Does an image search on Google and sends the results. \n"
            "Usage `.img [limit:int]? [format:str]? (search_query)`",
        'google':
            "Does a search on Google. \n"
            "Usage `.google [limit:int]? [page:int]? (search_query)`",
        'wiki':
            "Does a Wikipedia search. \n"
            "Usage: `.wiki (search_query)`",
        'ud':
            "Does a search on Urban Dictionary. \n"
            "Usage: `.ud (search_query)`",
        'tts':
            "Translates text to speech. \n"
            "Usage: `.tts [lang:str]? [slow:bool]? (message)?`",
        'trt':
            "Translates text using Google Translate. \n"
            "Usage: `.trt [to:str]? [from:str]? (message)?`",
        'lang':
            "Changes the default language of"
            "userbot scrapers used for Google TRT, "
            "TTS may not work. \n"
            "Usage: `.lang (lang)`",
        'yt':
            "Does a YouTube search. \n"
            "Usage: `.yt (search query)`",
        'ytdl':
            "Download videos from YouTube. "
            "If no resolution is specified, the highest downloadable quality is "
            "downloaded. Will send the link if the video is larger than 50 MB. \n"
            "Usage: `.ytdl [res:str]? (url)`",
        'ytmp3':
            "Download audio from YouTube. "
            "First fetches the video then converts it to an mp3. Might take some time. \n"
            "Usage: `.ytmp3 (url)`",
        'cr':
            "Currency converter, converts <from> to <to>. \n"
            "Usage: `.cr (amount) (from) (to)`"
    }
})