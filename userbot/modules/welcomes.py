# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
''' A module for helping ban group join spammers. '''

from asyncio import sleep

from telethon.events import ChatAction
from telethon.tl.functions.channels import EditBannedRequest, GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins, Message

from userbot.modules.misc import admins, make_mention
from userbot.modules.admin import spider as mute
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, WELCOME_MUTE, bot
from userbot.modules.admin import KICK_RIGHTS

RED_FLAG_WORDS = [
    'bitcoin', 'bitfenix', 'crypto', 'bitmex',
    'promotion', 'announce'
]

@bot.on(ChatAction)
async def welcome_mute(chat):
    """ Checks if a new user matches any of a number of conditions.
    If the user appears to be a spammer/bot does one of two things.
    
    1) If the current user is an admin, mutes the user immediately
       and notifies admins.
    2) If the current user is not an admin, notifies admins in the
       current chat of the potential bot."""

    # Make sure the welcome mute function is turned on
    if not WELCOME_MUTE:
        return

    user = await chat.get_user()
    user = await chat.client(GetFullUserRequest(user.id))
    full_name = ' '.join(list(filter(None, [user.first_name, user.last_name])))
    spam = False

    # Check the user's name for some red-flag words
    if any(flag in full_name for flag in RED_FLAG_WORDS):
        spam = True
    
    # Now check their bio
    elif any(flag in user.about for flag in RED_FLAG_WORDS):
        spam = True
    
    # Potential spam/bot user detected
    if spam:
        # If we're an admin in this chat go ahead and mute
        if chat.admin_rights or chat.creator:
            message = f"""There's a good chance this person is a spammer/bot.
            Muting just in case."""
            await chat.reply(message)
            await mute(chat)
        
        # Not an admin, so we'll just warn the admins
        else:
            # For now we're going to disable auto-mentioning of admins
            # mentions = map(make_mention, admins(chat))
            message = f"""There's a good chance this person is a spammer/bot"""
            await chat.reply(message)