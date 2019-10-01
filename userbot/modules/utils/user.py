# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# The entire source code is OSSRPL except 'user' which is MPL
# License: MPL and OSSRPL
""" Userbot module for getiing info
    about any user on Telegram(including you!). """

from telethon.events import NewMessage
from telethon.tl.custom import Message
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from ..help import add_help_item
from userbot.events import register
from userbot.utils import parse_arguments

TMP_DOWNLOAD_DIRECTORY = "./"


@register(pattern="^.u(?:ser)?(?: |$)(.*)?", outgoing=True)
async def who(event: NewMessage.Event):
    """ For .user command, get info about a user. """
    if event.fwd_from:
        return

    args, user = parse_arguments(event.pattern_match.group(1), [
        'id', 'forward', 'general', 'bot', 'misc', 'all', 'mention'
    ])

    args['forward'] = args.get('forward', True)
    args['user'] = user

    replied_user = await get_user(event, **args)
    caption = await fetch_info(replied_user, **args)

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        pass

    await event.edit(caption, parse_mode="markdown")


async def get_user(event: NewMessage.Event, **kwargs):
    """ Get the user from argument or replied message. """
    reply_msg: Message = await event.get_reply_message()
    user = kwargs.get('user', None)

    if user:
        # First check for a user id
        if user.isnumeric():
            user = int(user)

        # Then check for a user mention (@username)
        elif event.message.entities is not None:
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

    # Check for a forwarded message
    elif reply_msg and reply_msg.forward and kwargs['forward']:
        forward = reply_msg.forward
        replied_user = await event.client(
            GetFullUserRequest(forward.sender_id))

    # Check for a replied to message
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(
            GetFullUserRequest(previous_message.from_id))

    # Last case scenario is to get the current user
    else:
        self_user = await event.client.get_me()
        replied_user = await event.client(GetFullUserRequest(self_user.id))

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
        title = f"[{full_name}](tg://user?id={user.id}) \n"
    else:
        title = f"**{full_name}** \n"

    caption = title

    if id_only:
        caption += f"id: {user.id}"
        return caption

    if show_general:
        caption += "  **general** \n"
        caption += f"    id: `{user.id}` \n"
        caption += f"    first name: {user.first_name} \n"
        caption += f"    last name: {user.last_name} \n"
        caption += f"    username: {user.username} \n"
        caption += f"    mutual contact: {user.mutual_contact} \n"
        caption += f"    groups in common: {replied_user.common_chats_count} \n"

    if show_misc:
        caption += "  **misc** \n"
        caption += f"    restricted: {user.restricted} \n"
        caption += f"    restriction reason: {user.restriction_reason} \n"
        caption += f"    deleted: {user.deleted} \n"
        caption += f"    verified: {user.verified} \n"
        caption += f"    min: {user.min} \n"
        caption += f"    lang code: {user.lang_code} \n"

    if show_bot:
        caption += "  **bot info** \n"
        caption += f"    bot: {user.bot} \n"
        caption += f"    chat history: {user.bot_chat_history} \n"
        caption += f"    info version: {user.bot_info_version} \n"
        caption += f"    inline geo: {user.bot_inline_geo} \n"
        caption += f"    inline placeholder: {user.bot_inline_placeholder} \n"
        caption += f"    nochats: {user.bot_nochats} \n"

    return caption

add_help_item(
    ".user",
    "Utilities",
    "List information about a particular user.",
    """
    `.u(ser) [options] (username|id)`
    
    Or, in response to a message
    `.u(ser) [options]`
    
    Options:
    `.id`: Show only the user's ID (default: `False`)
    `.general`: Show general user info (default: `True`)
    `.bot`: Show bot related info (default: `False`)
    `.misc`: Show miscelanious info (default: `False`)
    `.all`: Show all info (overrides other options) (default: `False`)
    `.mention`: Inline mention the user (default: `False`)
    `.forward`: Follow forwarded message (default: `True`)
    """
)
