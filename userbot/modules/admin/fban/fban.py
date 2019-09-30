import asyncio

from telethon.tl.types import MessageEntityMentionName

from userbot import is_mongo_alive, is_redis_alive, bot
from userbot.events import register
from userbot.modules.dbhelper import get_fban


@register(outgoing=True, pattern="^.fban")
async def fedban_all(msg):
    if not is_mongo_alive() or not is_redis_alive():
        await msg.edit("`Database connections failing!`")
        return

    textx = await msg.get_reply_message()
    spamwatch = False

    if textx:
        try:
            banreason = "[userbot] "
            banreason += banreason.join(msg.text.split(" ")[1:])
            if banreason == "[userbot]":
                raise TypeError
        except TypeError:
            banreason = "[userbot] fban"
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
        if "spam" in banreason:
            spamwatch = True
    failed = dict()
    count = 1
    fbanlist = []
    x = (await get_fban())
    for i in x:
        fbanlist.append(i["chatid"])
    for bangroup in fbanlist:

        # Send to proof to Spamwatch in case it was spam
        # Spamwatch is a reputed fed fighting against spam on telegram

        if bangroup == -1001312712379:
            if spamwatch:
                if textx:
                    await textx.forward_to(-1001312712379)
                    # Tag him, coz we can't fban xd
                    await bot.send_message(-1001312712379, "@SitiSchu")
                else:
                    await msg.reply(
                        "`Spam message detected. But no reply message, can't forward to spamwatch`"
                    )
            continue
        async with bot.conversation(bangroup) as conv:
            await conv.send_message(f"!fban {banid} {banreason}")
            resp = await conv.get_response()
            await bot.send_read_acknowledge(conv.chat_id)
            if "Beginning federation ban " not in resp.text:
                failed[bangroup] = str(conv.chat_id)
            else:
                count += 1
                await msg.edit("`Fbanned on " + str(count) + " feds!`")
            # Sleep to avoid a floodwait.
            # Prevents floodwait if user is a fedadmin on too many feds
            await asyncio.sleep(0.2)
    if failed:
        failedstr = ""
        for i in failed.keys():
            failedstr += failed[i]
            failedstr += " "
        await msg.reply(f"`Failed to fban in {failedstr}`")
    else:
        await msg.reply("`Fbanned in all feds!`")
