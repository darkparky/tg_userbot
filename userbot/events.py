# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for managing events.
 One of the main components of the userbot. """

import asyncio
import sys
import traceback
from os import remove
from time import gmtime, strftime

from telethon import events

from userbot import bot, BOTLOG, BOTLOG_CHATID


def register(**args):
    """ Register a new event. """
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    group_only = args.get('group_only', False)
    disable_errors = args.get('disable_errors', False)
    incoming_func = args.get('incoming', True)
    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    if "disable_edited" in args:
        del args['disable_edited']

    if "group_only" in args:
        del args['group_only']

    if "disable_errors" in args:
        del args['disable_errors']

    def decorator(func):
        # noinspection PyBroadException
        async def wrapper(check):
            if group_only and not check.is_group:
                await check.respond("`Are you sure this is a group?`")
                return
            if incoming_func and not check.out:
                await func(check)
                return

            try:
                await func(check)
            except KeyboardInterrupt:
                pass
            except BaseException:

                # Check if we have to disable it. If not silence the log spam on the console, with a dumb except.

                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    text = "**Sorry, I encountered a error!**\n"

                    ftext = "\nDisclaimer:\nThis file is for your eyes "
                    ftext += "only and may contain sensitive data. Be "
                    ftext += "careful before sharing it with anyone. \n\n"
                    ftext += "--------BEGIN ERROR LOG--------"
                    ftext += "\nDate: " + date
                    ftext += "\nGroup ID: " + str(check.chat_id)
                    ftext += "\nSender ID: " + str(check.sender_id)
                    ftext += "\n\nEvent Trigger:\n"
                    ftext += str(check.text)
                    ftext += "\n\nTraceback info:\n"
                    ftext += str(traceback.format_exc())
                    ftext += "\n\nError text:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n--------END ERROR LOG--------"

                    command = "git log --pretty=format:\"%an: %s\" -5"

                    ftext += "\n\n\nLast 5 commits:\n"

                    process = await asyncio.create_subprocess_shell(
                        command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if BOTLOG:
                        await check.client.send_file(
                            BOTLOG_CHATID,
                            "error.log",
                            caption=text,
                        )
                    else:
                        await check.client.send_file(
                            check.chat_id,
                            "error.log",
                            caption=text,
                        )
                    remove("error.log")
            else:
                pass

        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
