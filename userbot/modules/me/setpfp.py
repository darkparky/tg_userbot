import os

from telethon.errors import PhotoCropSizeSmallError, ImageProcessFailedError, PhotoExtInvalidError
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from telethon.tl.types import MessageMediaPhoto

from ..help import add_help_item
from userbot import bot
from userbot.events import register

INVALID_MEDIA = "```The extension of the media entity is invalid.```"
PP_CHANGED = "```Profile picture changed successfully.```"
PP_TOO_SMOL = "```This image is too small, use a bigger image.```"
PP_ERROR = "```Failure occured while processing image.```"


@register(outgoing=True, pattern="^.setpfp")
async def set_profilepic(propic):
    """ For .setpfp command, change your profile picture in Telegram. """
    replymsg = await propic.get_reply_message()
    photo = None
    if replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await bot.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await bot.download_file(replymsg.media.document)
        else:
            await propic.edit(INVALID_MEDIA)

    if photo:
        try:
            await bot(UploadProfilePhotoRequest(await bot.upload_file(photo)))
            os.remove(photo)
            await propic.edit(PP_CHANGED)
        except PhotoCropSizeSmallError:
            await propic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await propic.edit(PP_ERROR)
        except PhotoExtInvalidError:
            await propic.edit(INVALID_MEDIA)


add_help_item(
    ".setpfp",
    "Me",
    "Set your profile pic.",
    """
    `.setpfp [with image]`
    
    Or, in response to an image
    `.setpfp`
    """
)
