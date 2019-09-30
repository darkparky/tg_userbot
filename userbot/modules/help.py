# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot help command """

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def show_help(event):
    """ For .help command,"""
    args = event.pattern_match.group(1)
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Please specify a valid module name.")
    else:
        await event.edit("Please specify which module do you want help for!")
        categories = list(CMD_HELP.keys())
        categories.sort()

        categorized = []
        misc = []

        for cat in categories:
            if type(CMD_HELP[cat]) == dict:
                items = ', '.join(CMD_HELP[cat].keys())
                message = f"**{cat}** \n"
                message += items
                categorized.append(message)
            else:
                misc.append(cat)

        message = '\n \n'.join(categorized)
        message += "\n \n **Misc** \n" + ', '.join(misc)
        await event.reply(message)
