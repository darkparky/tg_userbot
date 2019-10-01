import inspect

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import Channel, User

from userbot.utils import parse_arguments
from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern="^.c(?:hat)(.*|$)")
async def get_chat(e):
    params = e.pattern_match.group(1) or ""
    args, _ = parse_arguments(params, ['id'])

    reply_message = await e.get_reply_message()

    # TODO
    # if reply_message and reply_message.forward:
    #     chat = await reply_message.forward.get_chat()
    #     print(reply_message.forward.original_fwd)
    # else:
    #     chat = await e.get_chat()

    message = await fetch_info(e, **args)
    await e.edit(message)


async def fetch_info(event, **kwargs):
    chat = await event.get_chat()

    if isinstance(chat, User):
        from .user import fetch_info as fetch_user_info
        replied_user = await event.client(GetFullUserRequest(chat.id))
        return await fetch_user_info(replied_user, **kwargs)

    id_only = kwargs.get('id', False)
    print(chat)

    is_private = False
    if isinstance(chat, Channel) and chat.username:
        title = f"[{chat.username}](https://t.me/{chat.username})"
    elif chat.title:
        is_private = True
        title = f"**{chat.title}**"
    else:
        is_private = True
        title = f"**Chat {chat.id}**"

    if id_only:
        return title + f"\n  id: {chat.id}"

    caption = title + "\n"
    caption += "  **general** \n"
    caption += f"    id: {chat.id} \n"
    caption += f"    title: {chat.title} \n"
    caption += f"    private: {is_private} \n"
    caption += f"    participants: {chat.participants_count} \n"
    caption += f"    created at: {chat.date.strftime('%b %d %Y %H:%M:%S')} \n"

    return caption


add_help_item(
    ".chat",
    "Utilities",
    "Returns stats for the current chat.",
    """
    `.chat [options]`
    
    Options:
    `id`: Return only the id.
    """
)
