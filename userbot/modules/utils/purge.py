# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for purging unneeded messages(usually spam or ot). """

from telethon.errors import rpcbaseerrors

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.purge$")
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


@register(outgoing=True, pattern=r"^.purgeme\s?([0-9]+|all)?")
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


@register(outgoing=True, pattern="^.del$")
async def delete_it(delme):
    """ For .del command, delete the replied message. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Deletion of message was successful")
        except rpcbaseerrors.BadRequestError:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Well, I can't delete a message")


@register(outgoing=True, pattern="^.editme")
async def editer(edit):
    """ For .editme command, edit your last message. """
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id('me')
    string = str(message[8:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(BOTLOG_CHATID,
                                       "Edit query was executed successfully")


@register(outgoing=True, pattern=r"^.sd ([0-9]+) ([\S\s]+)")
async def selfdestruct(destroy):
    """ For .sd command, make self-destructable messages. """
    seconds = int(destroy.pattern_match.group(1))
    text = str(destroy.pattern_match.group(2))
    await destroy.edit(text, delete_in=seconds)


CMD_HELP["General"].update({
    'purge': '.purge'
             '\nUsage: Purge all messages starting from the reply.',
    'purgeme':
        '.purgeme <x>'
        '\nUsage: Delete x amount of your latest messages.',
    "del":
        ".del" "\nUsage: Delete the message you replied to.",
    'editme':
        ".editme <newmessage>"
        "\nUsage: Edit the text you replied to with newtext.",
    'sd':
        '.sd <x> <message>'
        "\nUsage: Create a message that self-destructs in x seconds."
        '\nKeep the seconds under 100 since it puts your bot to sleep.'
})
