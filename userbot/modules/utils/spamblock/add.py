import io

from PIL import Image
from Crypto.Hash import SHA512
from photohash import average_hash

from ...help import add_help_item
from userbot.events import register
from userbot.modules.dbhelper import get_file_hash, add_file_hash
from userbot.utils.tgdoc import *


@register(outgoing=True, pattern=r"^\.s(?:pam)?b(?:lock)? add photo$")
async def spamblock_add_pic(e):
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


@register(outgoing=True, pattern=r"^\.s(?:pam)?b(?:lock)? add file$")
async def spamblock_add_file(e):
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


# @register(outgoing=True, pattern=r"^\.s(?:pam)?b(?:lock)? add chat (\S+)$")
# async def spamblock_add_chat(e):
#     chat = e.pattern_match.group(1)
#     entity = await e.client.get_entity(chat)
#
#
#
#
# @register(outgoing=True, pattern=r"^\.s(?:pam)?b(?:lock)? add (?:key)?word ([\S\s]+)$")
# async def spamblock_add_keyword(e):
#     pass


add_help_item(
    ".spamblock add photo",
    "Utilities",
    "Get the average hash for a photo and add it "
    "to the blacklist.",
    """
    `.spamblock add photo`
    """
)

add_help_item(
    ".spamblock add file",
    "Utilities",
    "Get the hash for a file and add it "
    "to the blacklist.",
    """
    `.spamblock add file`
    """
)
