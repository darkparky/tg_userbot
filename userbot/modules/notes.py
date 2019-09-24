# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for keeping notes. """

from asyncio import sleep

from userbot import (BOTLOG, BOTLOG_CHATID, CMD_HELP, is_mongo_alive,
                     is_redis_alive)
from userbot.events import register
from userbot.modules.dbhelper import add_note, delete_note, get_note, get_notes


@register(outgoing=True, pattern=r"^.notes$")
async def notes_active(event):
    """ List all of the notes saved in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return

    message = "`There are no saved notes in this chat`"
    notes = await get_notes(event.chat_id)
    for note in notes:
        if message == "`There are no saved notes in this chat`":
            message = "Notes saved in this chat:\n"
            message += "🔹 **{}**\n".format(note["name"])
        else:
            message += "🔹 **{}**\n".format(note["name"])

    await event.edit(message)


@register(outgoing=True, pattern=r"^.delnote (.*)")
async def remove_notes(event):
    """Deletes the note with the given name"""
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    notename = event.pattern_match.group(1)
    if await delete_note(event.chat_id, notename) is False:
        return await event.edit("`Couldn't find note:` **{}**".format(notename)
                                )
    else:
        return await event.edit(
            "`Successfully deleted note:` **{}**".format(notename))
    
    sleep(1)
    await event.delete()


@register(outgoing=True, pattern=r'^.addnote (\w[\w\d_]+)\s?([\S\s]+)?')
async def add_filter(event):
    """ For .save command, saves notes in a chat. """
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
        
    notename = event.pattern_match.group(1)
    string = event.pattern_match.group(2)

    if event.reply_to_msg_id:
        string = (await event.get_reply_message()).text

    msg = "`Note {} successfully. Use` #{} `to get it`"

    if await add_note(event.chat_id, notename, string) is False:
        return await event.edit(msg.format('updated', notename))
    else:
        return await event.edit(msg.format('added', notename))
    
    sleep(1)
    await event.delete()

@register(pattern=r"#\w*",
          disable_edited=True,
          ignore_unsafe=True,
          disable_errors=True)
async def note(event):
    """ Notes logic. """
    try:
        me = await event.client.get_me()
        if not (await event.get_sender()).bot and (event.from_id == me.id):
            if not is_mongo_alive() or not is_redis_alive():
                return

            notename = event.text[1:]
            note = await get_note(event.chat_id, notename)
            if note:
                await event.reply(note["text"])
    except BaseException:
        pass

CMD_HELP["General"].update({
    "addnote":
        "Adds a note by name. \n" 
        "Usage: `.addnote (note name) (note content)`",
    "delnote":
        "Deletes a note by name. \n"
        "Usage: `.delnote (note name)`",
    "notes":
        "List all saved notes (names only). \n"
        "Usage: `.notes`"
})
