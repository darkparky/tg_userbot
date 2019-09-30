from telethon.errors import PhotoCropSizeSmallError, ImageProcessFailedError
from telethon.tl.functions.channels import EditPhotoRequest
from telethon.tl.types import MessageMediaPhoto

from userbot import bot
from userbot.events import register
from userbot.modules.admin import (NO_ADMIN, INVALID_MEDIA, CHAT_PP_CHANGED, PP_TOO_SMOL, PP_ERROR)


@register(outgoing=True, group_only=True, pattern="^.setgrouppic$")
async def set_group_photo(gpic):
    """ For .setgrouppic command, changes the picture of a group """
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    photo = None

    if not chat.admin_rights or chat.creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await bot.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await bot.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await EditPhotoRequest(gpic.chat_id, await bot.upload_file(photo))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)