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

from telethon.tl.types import ChannelParticipantsAdmins
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^r/(\S+)")
async def subreddit(r):
    sub = r.pattern_match.group(1)
    link = f"**[r/{sub}](https://reddit.com/r/{sub})**"

    await r.edit(link)

@register(outgoing=True, pattern="^([Oo]of)$")
async def Oof(e):
    t = e.pattern_match.group(1)
    for j in range(15):
        t = t[:-1] + "of"
        await e.edit(t)

@register(outgoing=True, pattern="^.linux")
async def linux_interjection(msg):
    reply_message = await msg.get_reply_message()
    await reply_message.reply("I'd just like to interject for a moment. What you’re referring to as Linux, is in fact, GNU/Linux, or as I’ve recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX. Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called “Linux”, and many of its users are not aware that it is basically the GNU system, developed by the GNU Project. There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine’s resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called “Linux” distributions are really distributions of GNU/Linux.")
    await msg.delete()

@register(outgoing=True, pattern="^.admins?")
async def admins(msg):
    admins = await msg.client.get_participants(msg.chat, filter=ChannelParticipantsAdmins)
    admins = map(lambda x: x if not x.bot else None, admins)
    admins = [i for i in list(admins) if i]
    mentions = map(make_mention, admins)
    response = ' '.join(mentions)

    reply_message = await msg.get_reply_message()

    await msg.client.send_message(msg.chat, response, reply_to=reply_message)
    await msg.delete()

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
        reply_text = 'Hmm... [Let Me Google That For You](http://lmgtfy.com/?s=g&iie=1&q=' + query.replace(" ", "+") + ")"
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

def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        names = [user.first_name, user.last_name]
        names = [i for i in list(names) if i]
        full_name = ' '.join(names)
        return f"[{full_name}](tg://user?id={user.id})"

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
