import inspect

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Channel, User

from userbot.utils import parse_arguments, list_admins, inline_mention
from ..help import add_help_item
from userbot.events import register
from userbot.utils.tgdoc import *


@register(outgoing=True, pattern=r"^\.c(?:hat)?(\s+[\S\s]+|$)")
async def chat_info(e):
    params = e.pattern_match.group(1) or ""
    args, _ = parse_arguments(params, ['id', 'general', 'admins', 'all'])

    reply_message = await e.get_reply_message()

    # TODO: Get information about the chat a message was forwarded from
    # if reply_message and reply_message.forward:
    #     chat = await reply_message.forward.get_chat()
    #     print(reply_message.forward.original_fwd)
    # else:
    #     chat = await e.get_chat()

    await e.edit("**Fetching chat info...**")
    response = await fetch_info(e, **args)
    await e.edit(str(response))


async def fetch_info(event, **kwargs):
    chat = await event.get_chat()

    if isinstance(chat, User):
        from .user import fetch_info as fetch_user_info
        replied_user = await event.client(GetFullUserRequest(chat.id))
        return await fetch_user_info(replied_user, **kwargs)

    show_all = kwargs.get('all', False)
    id_only = kwargs.get('id', False)
    show_general = kwargs.get('general', True)
    show_admins = kwargs.get('admins', False)

    is_private = False
    if isinstance(chat, Channel) and chat.username:
        title = Link(chat.username, f"https://t.me/{chat.username}")
    elif chat.title:
        is_private = True
        title = Bold(chat.title)
    else:
        is_private = True
        title = Bold(f"Chat {chat.id}")

    if show_all:
        show_general = True
        show_admins = True
    elif id_only:
        return KeyValueItem(title, Code(str(chat.id)))

    if show_general:
        participant_count = 0
        async for user in event.client.iter_participants(chat, aggressive=True):
            print(user)
            participant_count += 1

        general = SubSection(Bold("general"),
                             KeyValueItem("id", Code(str(chat.id))),
                             KeyValueItem("title", Code(chat.title)),
                             KeyValueItem("private", Code(str(is_private))),
                             KeyValueItem("participants", Code(str(participant_count))),
                             KeyValueItem("created at", Code(chat.date.strftime('%b %d %Y %H:%M:%S'))))
    else:
        general = None

    if show_admins:
        admin_list = await list_admins(event)
        admins = SubSection(Bold("admins"))
        for admin in admin_list:
            admins.items.append(String(inline_mention(admin)))
    else:
        admins = None

    return Section(
        general if show_general else None,
        admins if show_admins else None
    )


add_help_item(
    ".chat",
    "Utilities",
    "Returns stats for the current chat.",
    """
    `.chat [options]`
    
    Options:
    `.id`: Return only the id.
    `.general`: Show general information related to the chat.
    `.admins`: Show chat admins (does not mention them).
    `.all`: Show everything.
    """
)
