# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version
from shutil import which

import requests
from telethon import version

from userbot import CMD_HELP, is_mongo_alive, is_redis_alive, bot
from userbot.events import register
from userbot.utils.helpers import parse_arguments


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            neo = "neofetch --stdout"
            fetch = await asyncrunapp(
                neo,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("`Hella install neofetch first kthx`")


@register(outgoing=True, pattern="^.botver$")
async def bot_ver(event):
    """ For .botver command, get the bot version. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@",
                                                             "!"):
        if which("git") is not None:
            invokever = "git describe --all --long"
            ver = await asyncrunapp(
                invokever,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await ver.communicate()
            verout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            invokerev = "git rev-list --all --count"
            rev = await asyncrunapp(
                invokerev,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )
            stdout, stderr = await rev.communicate()
            revout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            await event.edit("`Userbot Version: "
                             f"{verout}"
                             "` \n"
                             "`Revision: "
                             f"{revout}"
                             "` \n"
                             "`Tagged Version: r4.0`")
        else:
            await event.edit(
                "Shame that you don't have git, You're running r4.0 anyway")


@register(outgoing=True, pattern="^.pip(?: |$)(.*)")
async def pipcheck(pip):
    """ For .pip command, do a pip search. """
    if not pip.text[0].isalpha() and pip.text[0] not in ("/", "#", "@", "!"):
        pipmodule = pip.pattern_match.group(1)
        if pipmodule:
            await pip.edit("`Searching . . .`")
            invokepip = f"pip3 search {pipmodule}"
            pipc = await asyncrunapp(
                invokepip,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await pipc.communicate()
            pipout = str(stdout.decode().strip()) \
                + str(stderr.decode().strip())

            if pipout:
                if len(pipout) > 4096:
                    await pip.edit("`Output too large, sending as file`")
                    file = open("output.txt", "w+")
                    file.write(pipout)
                    file.close()
                    await pip.client.send_file(
                        pip.chat_id,
                        "output.txt",
                        reply_to=pip.id,
                    )
                    remove("output.txt")
                    return
                await pip.edit("**Query: **\n`"
                               f"{invokepip}"
                               "`\n**Result: **\n`"
                               f"{pipout}"
                               "`")
            else:
                await pip.edit("**Query: **\n`"
                               f"{invokepip}"
                               "`\n**Result: **\n`No Result Returned/False`")
        else:
            await pip.edit("`Use .help pip to see an example`")

@register(outgoing=True, pattern="^.docs\s+(.*)")
async def doc_search(e):
    params = e.pattern_match.group(1)
    args, lib = parse_arguments(params)
    lib = lib.strip()

    version = int(args.get('version', 3))
    python_url = f"https://docs.python.org/{version}/library/{lib}.html"
    pip_url = f"https://pypi.org/project/{lib}/"
    
    await e.edit(f"Searching docs for `{lib}`...")
    if requests.get(python_url).status_code == 200:
        response = f"[Check out the Python {version} docs for {lib}]({python_url}).\nI think you'll find it useful."
    elif requests.get(pip_url).status_code == 200:
        readthedocs_url = f"https://readthedocs.org/projects/{lib}/"
        if requests.get(readthedocs_url).status_code == 200:
            response = f"[Check out the docs for {lib} on readthedocs]({readthedocs_url}).\nI think you'll find it useful."

    if response:
        await e.edit(response)
    else:
        await e.edit(f"No docs found for `{lib}`...", delete_in=3)


@register(outgoing=True, pattern="^.alive$")
async def amireallyalive(e):
    if not is_mongo_alive() and not is_redis_alive():
        db = "Both Mongo and Redis Database seems to be failing!"
    elif not is_mongo_alive():
        db = "Mongo DB seems to be failing!"
    elif not is_redis_alive():
        db = "Redis Cache seems to be failing!"
    else:
        db = "Databases functioning normally!"
    
    username = (await bot.get_me()).username
    await e.edit("`"
                 "Your bot is running \n\n"
                 f"Telethon version: {version.__version__} \n"
                 f"Python: {python_version()} \n"
                 f"User: @{username} \n"
                 f"Database Status: {db}"
                 "`")


CMD_HELP.update({
    "System": {
        "sysd":
            "Show system information using neofetch. \n"
            "Usage: `.sysd`",
        "botver":
            "Show the userbot version. \n"
            "Usage: `.botver`",
        "pip":
            "Search module(s) in PyPi. \n"
            "Usage: `.pip (module[s])`",
        "alive":
            "Check if your bot is working or not. \n"
            "Usage: `.alive`"
    }
})
