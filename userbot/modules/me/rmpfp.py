from telethon.tl.functions.photos import GetUserPhotosRequest, DeletePhotosRequest
from telethon.tl.types import InputPhoto

from userbot import bot
from userbot.events import register


@register(outgoing=True, pattern=r"^.rmpfp")
async def remove_profilepic(delpfp):
    """ For .rmpfp command, delete your current
        profile picture in Telegram. """
    group = delpfp.text[6:]
    if group == 'all':
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1

    pfplist = await bot(
        GetUserPhotosRequest(user_id=delpfp.from_id,
                             offset=0,
                             max_id=0,
                             limit=lim))
    input_photos = []
    for sep in pfplist.photos:
        input_photos.append(
            InputPhoto(id=sep.id,
                       access_hash=sep.access_hash,
                       file_reference=sep.file_reference))
    await bot(DeletePhotosRequest(id=input_photos))
    await delpfp.edit(
        f"`Successfully deleted {len(input_photos)} profile picture(s).`")
