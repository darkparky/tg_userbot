# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except
# 'download, uploadir, uploadas, upload' which is MPL
# License: MPL and OSSRPL
""" Userbot module which contains everything related to
    downloading/uploading from/to the server. """

import logging
import mimetypes
import os
import re
from datetime import datetime
from io import BytesIO
from time import sleep

import psutil
from pyDownload import Downloader
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from telethon.tl.types import MessageMediaPhoto

from userbot import GDRIVE_FOLDER, LOGS
from userbot.events import register

TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY", "./")

@register(pattern=r"^.mirror(?: |$)([\s\S]*)", outgoing=True)
async def gdrive_mirror(request):
    """ Download a file and upload to Google Drive """
    message = request.pattern_match.group(1)
    if not request.reply_to_msg_id and not message:
        await request.edit("Usage: `.mirror <url>|<filename?>`", delete_in=3)
        return
    reply = ''
    reply_msg = await request.get_reply_message()
    links = re.findall(r"\bhttps?://.*\.\S+", message)
    if not (links or reply_msg or reply_msg.media or reply_msg.media.document):
        reply = "`No links or telegram files found!`\n"
        await request.edit(reply)
        return
    if request.reply_to_msg_id:
        await request.edit('Downloading from Telegram...')
        filen, buf = await download_from_tg(request)
        await request.edit(f'Uploading `{filen}` to GDrive...')
        reply += await gdrive_upload(
            filen, buf) if buf else await gdrive_upload(filen)
    elif "|" in message:
        url, file_name = message.split("|")
        url = url.strip()
        file_name = file_name.strip()
        await request.edit(f'Downloading `{file_name}`')
        status = await download_from_url(url, file_name)
        await request.edit(status)
        await request.edit(f'Uploading `{file_name}` to GDrive...')
        reply += await gdrive_upload(file_name)
    if "NoSecret" in reply:
        reply = "Run the `generate_drive_session.py` file " \
                "in your machine to authenticate on Google Drive!!`"
        return await request.edit(reply, delete_in=3)
    await request.edit(reply)


def progress(current, total):
    """ Logs the download progress """
    LOGS.info("Downloaded %s of %s\nCompleted %s", current, total,
              (current / total) * 100)


async def download_from_url(url: str, file_name: str) -> str:
    """
    Download files from URL
    """
    start = datetime.now()
    downloader = Downloader(url=url)
    if downloader.is_running:
        sleep(1)
    end = datetime.now()
    duration = (end - start).seconds
    os.rename(downloader.file_name, file_name)
    status = f"Downloaded `{file_name}` in {duration} seconds."
    return status


async def download_from_tg(target_file) -> (str, BytesIO):
    """
    Download files from Telegram
    """
    async def dl_file(buffer: BytesIO) -> BytesIO:
        buffer = await target_file.client.download_media(
            reply_msg,
            buffer,
            progress_callback=progress,
        )
        return buffer

    start = datetime.now()
    buf = BytesIO()
    reply_msg = await target_file.get_reply_message()
    avail_mem = psutil.virtual_memory().available + psutil.swap_memory().free
    try:
        if reply_msg.media.document.size >= avail_mem:  # unlikely to happen but baalaji crai
            filen = await target_file.client.download_media(
                reply_msg,
                progress_callback=progress,
            )
        else:
            buf = await dl_file(buf)
            filen = reply_msg.media.document.attributes[0].file_name
    except AttributeError:
        buf = await dl_file(buf)
        try:
            filen = reply_msg.media.document.attributes[0].file_name
        except AttributeError:
            if isinstance(reply_msg.media, MessageMediaPhoto):
                filen = 'photo-' + str(datetime.today())\
                    .split('.')[0].replace(' ', '-') + '.jpg'
            else:
                filen = reply_msg.media.document.mime_type\
                    .replace('/', '-' + str(datetime.today())
                             .split('.')[0].replace(' ', '-') + '.')
    end = datetime.now()
    duration = (end - start).seconds
    await target_file.edit(f"Downloaded `{filen}` in `{duration}` seconds.")
    return filen, buf


async def gdrive_upload(filename: str, filebuf: BytesIO = None) -> str:
    """
    Upload files to Google Drive using PyDrive
    """
    drive = drive_auth()

    if filename.count('/') > 1:
        filename = filename.split('/')[-1]
    filedata = {
        'title': filename,
        "parents": [{
            "kind": "drive#fileLink",
            "id": GDRIVE_FOLDER
        }]
    }

    if filebuf:
        mime_type = mimetypes.guess_type(filename)
        if mime_type[0]:
            filedata['mimeType'] = mime_type[0]
        else:
            filedata['mimeType'] = 'text/plain'
        file = drive.CreateFile(filedata)
        file.content = filebuf
    else:
        file = drive.CreateFile(filedata)
        file.SetContentFile(filename)
    name = filename.split('/')[-1]
    print(filename)
    print(file)
    file.Upload()
    # insert new permission
    file.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader'
    })
    if not filebuf:
        os.remove(filename)
    reply = f"[{name}]({file['alternateLink']})"
    return reply


def drive_auth():
    # a workaround for disabling cache errors
    # https://github.com/googleapis/google-api-python-client/issues/299
    logging.getLogger('googleapiclient.discovery_cache').setLevel(
        logging.CRITICAL)

    # Authenticate Google Drive automatically
    # https://stackoverflow.com/a/24542604
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("secret.json")
    if gauth.credentials is None:
        raise Exception("NoSecret: Failed to authenticate with Google Drive")
    if gauth.access_token_expired:
        gauth.Refresh()
    else:
        # Initialize the saved credentials
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("secret.json")
    return GoogleDrive(gauth)