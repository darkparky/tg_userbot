# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands
    for interacting with dogbin(https://del.dog)"""

from requests import exceptions, get, post

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

DOGBIN_URL = "https://del.dog/"


@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)")
async def paste(pstl):
    """ For .paste command, allows using
        dogbin functionality with the command. """
    dogbin_final_url = ""

    match = pstl.pattern_match.group(1).strip()
    reply_id = pstl.reply_to_msg_id
    if not match and not reply_id:
        await pstl.edit("There's nothing to paste.")
        return

    if match:
        message = match
    elif reply_id:
        message = (await pstl.get_reply_message()).message

    # Dogbin
    await pstl.edit("`Pasting text . . .`")
    resp = post(DOGBIN_URL + "documents", data=message.encode('utf-8'))

    if resp.status_code == 200:
        response = resp.json()
        key = response['key']
        dogbin_final_url = DOGBIN_URL + key

        if response['isUrl']:
            reply_text = ("`Pasted successfully!`\n\n"
                          f"`Shortened URL:` {dogbin_final_url}\n\n"
                          "Original(non-shortened) URLs`\n"
                          f"`Dogbin URL`: {DOGBIN_URL}v/{key}\n")
        else:
            reply_text = ("`Pasted successfully!`\n\n"
                          f"`Dogbin URL`: {dogbin_final_url}")
    else:
        reply_text = ("`Failed to reach Dogbin`")

    await pstl.edit(reply_text)
    if BOTLOG:
        await pstl.client.send_message(
            BOTLOG_CHATID,
            "Paste query `" + message + "` was executed successfully",
        )


CMD_HELP["General"].update({
    "paste":
        "Create a paste or a shortened url using "
        "dogbin (https://del.dog/)",
    "pastestats":
        "Get stats of a paste or shortened "
        "url from dogbin (https://del.dog/)"
})