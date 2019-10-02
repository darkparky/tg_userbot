from telethon.errors import PhotoCropSizeSmallError, ImageProcessFailedError
from telethon.tl.functions.channels import EditPhotoRequest
from telethon.tl.types import MessageMediaPhoto

from ..help import add_help_item
from userbot import bot
from userbot.events import register
from userbot.modules.admin import (NO_ADMIN, INVALID_MEDIA, CHAT_PP_CHANGED, PP_TOO_SMOL, PP_ERROR)


@register(outgoing=True, group_only=True, pattern="^.setchatpic$")
async def set_group_photo(e):
    """ For .setchatpic command, changes the picture of a chat """
    replymsg = await e.get_reply_message()
    chat = await e.get_chat()
    photo = None

    if not chat.admin_rights or chat.creator:
        await e.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await bot.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await bot.download_file(replymsg.media.document)
        else:
            await e.edit(INVALID_MEDIA)

    if photo:
        try:
            e.client(EditPhotoRequest(e.chat_id, await bot.upload_file(photo)))
            await e.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await e.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await e.edit(PP_ERROR)


add_help_item(
    ".setchatpic",
    "Admin",
    "Set the profile pic for the current chat.",
    """
    `.setchatpic [with an image]`
    
    Or, in reply to a message with an image
    `.setchatpic`
    """
)
