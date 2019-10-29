import io

from PIL import Image
from Crypto.Hash import SHA512
from photohash import average_hash

from ...help import add_help_item
from userbot.events import register
from userbot.modules.dbhelper import get_file_hash, add_file_hash
from userbot.utils.tgdoc import *


@register(outgoing=True, pattern=r"^\.s(?:pam)?b(?:lock)?\s+add\s+(\S+)(?:\s+([\S\s]+)|$)")
async def spamblock_add(e):
    command = e.pattern_match.group(1)
    opts = e.pattern_match.group(2)

    if command in ["photo", "pic"]:
        await _add_photo(e, opts)
    elif command == "file":
        await _add_file(e, opts)
    elif command in ["chat", "group", "channel"]:
        await _add_chat(e, opts)
    elif command in ["site", "domain"]:
        await _add_domain(e, opts)


async def _add_photo(e, opts):
    reply = await e.get_reply_message()
    message = reply if reply else e.message

    if message.photo:
        await e.edit("**Downloading photo...**")
    else:
        await e.edit("**Choose a file to add**", delete_in=3)
        return

    photo = io.BytesIO()
    await message.download_media(file=photo)

    image = Image.open(photo)
    _hash = average_hash(image)

    if await add_file_hash(_hash, 'pic'):
        message = TGDoc(Section(
            Bold("Added file"),
            KeyValueItem(Bold("photo"), Code(_hash))
        ))
        await e.edit(str(message))
    else:
        await e.edit("**Failed to add photo**", delete_in=3)


async def _add_file(e, opts):
    reply = await e.get_reply_message()
    message = reply if reply else e.message

    if message.file:
        await e.edit("**Downloading file...**")
    else:
        await e.edit("**Choose a file to add**", delete_in=3)
        return

    file = io.BytesIO()
    await message.download_media(file=file)

    print(len(file.getvalue()))

    await e.edit("**Calculating SHA512 hash for file...**")
    sha_hash = SHA512.new()
    sha_hash.update(file.getvalue())
    digest = sha_hash.hexdigest()

    if await add_file_hash(digest, 'file'):
        message = TGDoc(Section(
            Bold("Added file"),
            KeyValueItem(Bold("file"), Code(digest[:16] + '...'))
        ))
        await e.edit(str(message))
    else:
        await e.edit("**Failed to add file**", delete_in=3)


async def _add_chat(e, opts):
    pass


async def _add_domain(e, opts):
    pass


add_help_item(
    ".sb add photo",
    "Utilities",
    "Get the average hash for a photo and add it "
    "to the blacklist.",
    """
    `.sb add photo`
    """
)

add_help_item(
    ".sb add file",
    "Utilities",
    "Get the hash for a file and add it "
    "to the blacklist.",
    """
    `.sb add file`
    """
)
