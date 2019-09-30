# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands
    for interacting with dogbin(https://del.dog)"""

from requests import post

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

DOGBIN_URL = "https://del.dog/"


@register(outgoing=True, pattern=r"^.paste(?: |$)([\s\S]*)?")
async def paste(pstl):
    """ For .paste command, allows using
        dogbin functionality with the command. """

    match = pstl.pattern_match.group(1)
    reply_message = await pstl.get_reply_message()
    if not match and not reply_message:
        await pstl.edit("There's nothing to paste.")
        return

    if match:
        message = match.strip()
    elif reply_message:
        message = reply_message.message.strip()
    else:
        pstl.edit("Give me something to paste", delete_in=3)
        return

    # Dogbin
    await pstl.edit("`Pasting text . . .`")
    resp = post(DOGBIN_URL + "documents", data=message.encode('utf-8'))

    if resp.status_code == 200:
        response = resp.json()
        key = response['key']
        dogbin_final_url = DOGBIN_URL + key

        print(response)

        if response['isUrl']:
            reply_text = ("`Pasted successfully!`\n\n"
                          f"`Shortened URL:` {dogbin_final_url}\n\n"
                          "Original(non-shortened) URLs`\n"
                          f"`Dogbin URL`: {DOGBIN_URL}v/{key}\n")
        else:
            reply_text = ("`Pasted successfully!`\n\n"
                          f"`Dogbin URL`: {dogbin_final_url}")
    else:
        reply_text = "`Failed to reach Dogbin`"

    await pstl.edit(reply_text)
    if BOTLOG:
        await pstl.client.send_message(
            BOTLOG_CHATID,
            "Paste query `" + message + "` was executed successfully",
        )


CMD_HELP["General"].update({
    "paste":
        "Create a paste or a shortened url using "
        "dogbin (https://del.dog/)"
})