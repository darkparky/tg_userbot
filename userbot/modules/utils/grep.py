import re

from telethon.errors import MessageNotModifiedError

from ..help import add_help_item
from userbot.events import register
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^.grep(?:\s+)([\S\s]+)")
async def grep_messages(e):
    params = e.pattern_match.group(1)
    args, pattern = parse_arguments(params, [
        'regex', 'chatlimit', 'msglimit', 'groups', 'channels',
        'users', 'archived', 'ids', 'quiet', 'from'
    ])

    use_regex = args.get('regex', False)
    quiet = args.get('quiet', False)
    chatlimit = int(args['chatlimit']) if args.get('chatlimit') else None
    msglimit = int(args['msglimit']) if args.get('msglimit') else None
    reverse = args.get('reverse', False)
    from_user = int(args.get('from')) if str(args.get('from')).isnumeric() else args.get('from')
    groups = args.get('groups', True)
    channels = args.get('channels', True)
    users = args.get('users', True)
    archived = args.get('archived', False)
    # ids = args.get('ids', "").split(r",\s?")
    ids = None

    if not pattern:
        e.edit("Give me something to grep", delete_in=3)
        return

    matches = {}
    chat_count = 0
    async for dialog in e.client.iter_dialogs(archived=archived):
        if dialog.is_group and not groups:
            continue
        if dialog.is_channel and not channels:
            continue
        if dialog.is_user and not users:
            continue

        chat_count += 1
        if chat_count > chatlimit:
            break

        if not quiet:
            try:
                await e.edit(f"Searching {dialog.title}...")
            except MessageNotModifiedError:
                pass

        if use_regex:
            async for message in e.client.iter_messages(
                    dialog.id,
                    limit=msglimit,
                    reverse=reverse,
                    from_user=from_user,
                    ids=ids):

                if re.match(pattern, message.text):
                    if not matches.get(dialog.title):
                        matches.update({dialog.title: {}})

                    matches[dialog.title].update(message)

        else:
            async for message in e.client.iter_messages(
                    dialog.id,
                    limit=msglimit,
                    reverse=reverse,
                    from_user=from_user,
                    ids=ids,
                    search=pattern):

                if not matches.get(dialog.title):
                    matches.update({dialog.title: []})

                print(message.text + "\n")
                matches[dialog.title].append(message)

    print(matches)
    message = "**Search results** \n"
    for chat in matches.keys():
        message += f"  **{chat}** \n"
        for msg in matches[chat]:
            message += f"    [{msg.post_author}](tg://user?id={msg.from_id}) \n"
            message += f"    {msg.text}"
        message += '\n'

    await e.edit(message)
