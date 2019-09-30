import os
import shutil

from google_images_download import google_images_download

from userbot.events import register
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^.img (.*)")
async def img_sampler(event):
    """ For .img command, search and return images matching the query. """
    await event.edit("Processing query...")

    query = event.pattern_match.group(1)
    opts, query = parse_arguments(query)
    limit = opts.get('limit', 3)
    fmt = opts.get('format', 'jpg')

    response = google_images_download.googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": limit,
        "format": fmt,
        "no_directory": "no_directory"
    }

    # passing the arguments to the function
    await event.edit("Downloading images...")
    paths = response.download(arguments)
    lst = paths[0][query]

    await event.edit(f"Sending {limit} images...")
    await event.client.send_file(event.chat_id, lst)

    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()