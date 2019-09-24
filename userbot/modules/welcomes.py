# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
''' A module for helping ban group join spammers. '''


from telethon.events import ChatAction
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChannelParticipantsAdmins, Message

from userbot.modules.admin import MUTE_RIGHTS
from userbot.modules.misc import admins, make_mention
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, WELCOME_MUTE, bot
from userbot.modules.admin import KICK_RIGHTS

RED_FLAG_WORDS = [
    'bitcoin', 'bitfenix', 'crypto', 'bitmex',
    'promotion', 'announce'
]

@bot.on(ChatAction)
async def welcome_mute(event):
    """ Checks if a new user matches any of a number of conditions.
    If the user appears to be a spammer/bot does one of two things.
    
    1) If the current user is an admin, mutes the user immediately
       and notifies admins.
    2) If the current user is not an admin, notifies admins in the
       current chat of the potential bot."""

    # Make sure the welcome mute function is turned on
    if not WELCOME_MUTE:
        return

    # Only run on joins and adds
    if not (event.user_joined or event.user_added):
        return

    message = event.action_message
    user = await event.get_user()
    user_full = await event.client(GetFullUserRequest(user.id))
    names = [str(user.first_name).lower(), str(user.last_name).lower()]
    
    spam = False

    # Check the user's name for some red-flag words
    if any(i in names for i in RED_FLAG_WORDS):
        spam = True
    
    # Now check their bio
    if any(flag in RED_FLAG_WORDS for flag in str(user_full.about)):
        spam = True
    
    print(f"Spam: {spam}")

    # Potential spam/bot user detected
    if spam:
        # If we're an admin in this chat go ahead and mute
        if message.chat.admin_rights or message.chat.creator:
            response = "There's a good chance this person is a spammer/bot"
            await message.reply(response)
        
        # Not an admin, so we'll just warn the admins
        else:
            # For now we're going to disable auto-mentioning of admins
            # mentions = map(make_mention, await admins(chat))
            response = "There's a good chance this person is a spammer/bot"
            await message.reply(response)

        # if BOTLOG:
        #     user_mention = make_mention(user)
        #     await message.client.send_message(
        #         BOTLOG_CHATID,
        #         f"Possible bot/spammer {user_mention} muted")