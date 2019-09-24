# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'user' which is MPL
# License: MPL and OSSRPL
""" Userbot module for getiing info
    about any user on Telegram(including you!). """

import os

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from userbot import CMD_HELP
from userbot.events import register
from userbot.utils.helpers import parse_arguments

TMP_DOWNLOAD_DIRECTORY = "./"


@register(pattern="^.u(?:ser)?(?: |$)(.*)", outgoing=True)
async def who(event):
    """ For .user command, get info about a user. """
    if event.fwd_from:
        return

    if not os.path.isdir(TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TMP_DOWNLOAD_DIRECTORY)

    args, user = parse_arguments(event.pattern_match.group(1))
    replied_user = await get_user(event, user)
    caption = await fetch_info(replied_user, **args)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    await event.edit(caption, parse_mode="markdown")

async def get_user(event, user):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))
    else:
        if user.isnumeric():
            user = int(user)

        if not user:
            self_user = await event.client.get_me()
            user = self_user.id

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(
                GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return replied_user


async def fetch_info(replied_user, **kwargs):
    """ Get details from the User object. """
    user = replied_user.user

    id_only = kwargs.get('id', False)
    show_general = kwargs.get('general', True)
    show_bot = kwargs.get('bot', False)
    show_misc = kwargs.get('misc', False)
    show_all = kwargs.get('all', False)
    mention_name = kwargs.get('mention', False)
    
    if show_all:
        show_general = True
        show_bot = True
        show_misc = True

    full_name = str(user.first_name + ' ' + (user.last_name or ''))

    if mention_name:
        title = f"**[{full_name}](tg://user?id={user.id})** \n"
    else:
        title = f"**{full_name}** \n"

    caption =  title
    
    if id_only:
        caption += f"id: {user.id}"
        return caption

    if show_general:
        caption +=  "  **general:** \n"
        caption += f"    id: `{user.id}` \n"
        caption += f"    first name: {user.first_name} \n"
        caption += f"    last name: {user.last_name} \n"
        caption += f"    username: {user.username} \n"
        caption += f"    mutual contact: {user.mutual_contact} \n"
        caption += f"    groups in common: {replied_user.common_chats_count} \n"

    if show_bot:
        caption +=  "  **bot info:** \n"
        caption += f"    bot: {user.bot} \n"
        caption += f"    chat history: {user.bot_chat_history} \n"
        caption += f"    info version: {user.bot_info_version} \n"
        caption += f"    inline geo: {user.bot_inline_geo} \n"
        caption += f"    inline placeholder: {user.bot_inline_placeholder} \n"
        caption += f"    nochats: {user.bot_nochats} \n"

    if show_misc:
        caption +=  "  **misc:** \n"
        caption += f"    restricted: {user.restricted} \n"
        caption += f"    restriction reason: {user.restriction_reason} \n"
        caption += f"    deleted: {user.deleted} \n"
        caption += f"    verified: {user.verified} \n"
        caption += f"    min: {user.min} \n"
        caption += f"    lang code: {user.lang_code} \n"

    return caption


CMD_HELP["General"].update({
    "user":
        "Get info about a user. \n"
        "Usage: `.u(ser) [options] (username|id)?` \n"
        "Options: (`.` prefix means true, `!` means false) \n"
        "  `.id`: Show only the user's ID (default: `False`) \n"
        "  `.general`: Show general user info (default: `True`) \n"
        "  `.bot`: Show bot related info (default: `False`) \n"
        "  `.misc`: Show miscelanious info (default: `False`) \n"
        "  `.all`: Show all info (overrides other options) (default: `False`) \n"
        "  `.mention`: Inline mention the user (default: `False`)"
})
