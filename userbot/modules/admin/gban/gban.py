import asyncio

from telethon.tl.types import MessageEntityMentionName

from userbot import is_mongo_alive, is_redis_alive, bot
from userbot.events import register
from userbot.modules.dbhelper import get_gban


@register(outgoing=True, pattern=r"^\.gban")
async def gban_all(msg):
    if not is_mongo_alive() or not is_redis_alive():
        await msg.edit("`Database connections failing!`")
        return
    textx = await msg.get_reply_message()
    if textx:
        try:
            banreason = "[userbot] "
            banreason += banreason.join(msg.text.split(" ")[1:])
            if banreason == "[userbot]":
                raise TypeError
        except TypeError:
            banreason = "[userbot] gban"
    else:
        banid = msg.text.split(" ")[1]
        if banid.isnumeric():
            # if its a user id
            banid = int(banid)
        else:
            # deal wid the usernames
            if msg.message.entities is not None and isinstance(msg.message.entities[0],
                                                               MessageEntityMentionName):
                ban_id = msg.message.entities[0].user_id
        try:
            banreason = "[userbot] "
            banreason += banreason.join(msg.text.split(" ")[2:])
            if banreason == "[userbot]":
                raise TypeError
        except TypeError:
            banreason = "[userbot] fban"
    if not textx:
        await msg.edit(
            "Reply Message missing! Might fail on many bots! Still attempting Gban!"
        )
        # Ensure User Read the warning
        await asyncio.sleep(1)
    x = (await get_gban())
    count = 0
    banlist = []
    for i in x:
        banlist.append(i["chatid"])
    for banbot in banlist:
        async with bot.conversation(banbot) as conv:
            if textx:
                c = await msg.forward_to(banbot)
                await c.reply("/id")
            await conv.send_message(f"/gban {banid} {banreason}")
            await bot.send_read_acknowledge(conv.chat_id)
            count += 1
            # We cant see if he actually Gbanned. Let this stay for now
            await msg.edit("`Gbanned on " + str(count) + " bots!`")
            await asyncio.sleep(0.2)
