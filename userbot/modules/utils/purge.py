# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for purging unneeded messages(usually spam or ot). """

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register


@register(outgoing=True, pattern=r"^\.purge$")
async def fastpurger(purg):
    """ For .purge command, purge all messages starting from the reply. """
    chat = await purg.get_input_chat()
    msgs = []
    count = 0

    async for msg in purg.client.iter_messages(chat,
                                               min_id=purg.reply_to_msg_id):
        msgs.append(msg)
        count = count + 1
        msgs.append(purg.reply_to_msg_id)
        if len(msgs) == 100:
            await purg.client.delete_messages(chat, msgs)
            msgs = []

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    await purg.respond(
        "`Fast purge complete!\n`Purged " + str(count) +
        " messages. **This auto-generated message " +
        "  shall be self destructed in 2 seconds.**",
        delete_in=2
    )

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "Purge of " + str(count) + " messages done successfully.")


@register(outgoing=True, pattern=r"^\.purgeme\s?([0-9]+|all)?")
async def purgeme(delme):
    """ For .purgeme, delete x count of your latest message."""
    count = delme.pattern_match.group(1)
    delall = False
    i = 1

    if count.lower() == 'all':
        delall = True
    elif count.isnumeric():
        count = int(count)
    else:
        await delme.respond(
            "First argument to `.purgeme` must be "
            "a number or `all`.",
            delete_in=2
        )

    async for message in delme.client.iter_messages(delme.chat_id,
                                                    from_user='me'):
        if not delall and (i > count + 1):
            break

        i = i + 1
        await message.delete()

    await delme.respond(
        "`Purge complete!` Purged " + str(count) +
        " messages. **This auto-generated message " +
        " shall be self destructed in 2 seconds.**",
        delete_in=2
    )

    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "Purge of " + str(count) + " messages done successfully.")


add_help_item(
    ".purge",
    "Utilities",
    "Purges all messages starting from the reply message.",
    """
    In reply to a message
    `.purge`
    """
)

add_help_item(
    ".purgeme",
    "Utilities",
    "Purges `n` of your messages going back.",
    """
    `.purgeme (num)`
    """
)