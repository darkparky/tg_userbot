# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import sys
from os import execl
from random import randint
from time import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^Oof$")
async def Oof(e):
    t = "Oof"
    for j in range(15):
        t = t[:-1] + "of"
        await e.edit(t)

@register(outgoing=True, pattern="^.lfy(?: |$)(.*)",)
async def let_me_google_that_for_you(lmgtfy):
    if not lmgtfy.text[0].isalpha() and lmgtfy.text[0] not in ("/", "#", "@", "!"):
        textx = await lmgtfy.get_reply_message()
        query = lmgtfy.text
        if query[5:]:
            query = str(query[5:])
        elif textx:
            query = textx
            query = query.message
        reply_text = 'Hmm, [Let Me Google That For You](http://lmgtfy.com/?s=g&iie=1&q=' + query.replace(" ", "+") + ")"
        await lmgtfy.edit(reply_text)

@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()

    if len(itemo) < 2:
        await items.edit("`2 or more items are required! Check "
                         ".help random for more info.`")
        return

    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    if " " not in time.pattern_match.group(1):
        await time.reply("Syntax: `.sleep [seconds]`")
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit("`I am sulking and snoozing....`")
        sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "You put the bot to sleep for " + str(counter) + " seconds",
            )
        sleep(counter)


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Goodbye *Windows XP shutdown sound*....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot shut down")
    await event.client.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def knocksomesense(event):
    await event.edit("`Hold tight! I just need a second to be back up....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot Restarted")
    await event.client.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()

@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit("https://github.com/watzon/tg_userbot/")


CMD_HELP.update({
    'random':
    ".random <item1> <item2> ... <itemN>"
    "\nUsage: Get a random item from the list of items."
})

CMD_HELP.update({
    'sleep':
    '.sleep 10'
    '\nUsage: Userbots get tired too. Let yours snooze for a few seconds.'
})

CMD_HELP.update({
    "shutdown":
    ".shutdown"
    '\nUsage: Sometimes you need to restart your bot. Sometimes you just hope to'
    "hear Windows XP shutdown sound... but you don't."
})

CMD_HELP.update(
    {'support': ".support"
     "\nUsage: If you need help, use this command."})

CMD_HELP.update({
    'repo':
    '.repo'
    '\nUsage: If you are curious what makes Paperplane work, this is what you need.'
})
