import inspect

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Channel, User

from userbot.utils import parse_arguments, list_admins, inline_mention
from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.c(?:hat)?(.*|$)")
async def get_chat(e):
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
    message = await fetch_info(e, **args)
    await e.edit(message)


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
        title = f"[{chat.username}](https://t.me/{chat.username}) \n"
    elif chat.title:
        is_private = True
        title = f"**{chat.title}** \n"
    else:
        is_private = True
        title = f"**Chat {chat.id}** \n"

    if show_all:
        show_general = True
        show_admins = True
    elif id_only:
        return title + f"  id: {chat.id}"

    caption = title

    if show_general:
        participant_count = 0
        async for user in event.client.iter_participants(chat, aggressive=True):
            print(user)
            participant_count += 1

        caption += "  **general** \n"
        caption += f"    id: {chat.id} \n"
        caption += f"    title: {chat.title} \n"
        caption += f"    private: {is_private} \n"
        caption += f"    participants: {participant_count} \n"
        caption += f"    created at: {chat.date.strftime('%b %d %Y %H:%M:%S')} \n"

    if show_admins:
        admins = await list_admins(event)
        caption += "  **admins** \n"
        for admin in admins:
            caption += f"    {inline_mention(admin)} \n"

    return caption


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
