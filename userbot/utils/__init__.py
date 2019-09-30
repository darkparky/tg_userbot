from re import findall, match

from telethon.tl.types import MessageEntityMentionName, ChannelParticipantsAdmins


def parse_arguments(message):
    options = {}

    # Handle boolean values
    for opt in findall(r"\s+([.!]\S+)\s+", message):
        if opt[0] == '.':
            options[opt[1:]] = True
        elif opt[0] == '!':
            options[opt[1:]] = False
        message = message.replace(opt, '')
    
    # Handle key/value pairs
    for opt in findall(r"\s+(\S+):(\S+)\s+", message):
        key, value = opt
        if value.isnumeric(): value = int(value)
        elif match(r"[Tt]rue|[Ff]alse", value): match(r"[Tt]rue", value)
        options[key] = value
        message = message.replace(':'.join(opt), '')

    return (options, message.strip())

def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d

def extract_urls(message):
    matches = findall(r'(https?://\S+)', str(message))
    return list(matches)

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    else:
        user = event.pattern_match.group(1)

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None

    return user_obj


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None

    return user_obj


async def admins(msg):
    adms = await msg.client.get_participants(msg.chat, filter=ChannelParticipantsAdmins)
    adms = map(lambda x: x if not x.bot else None, adms)
    adms = [i for i in list(adms) if i]
    return adms


def make_mention(user):
    if user.username:
        return f"@{user.username}"
    else:
        names = [user.first_name, user.last_name]
        names = [i for i in list(names) if i]
        full_name = ' '.join(names)
        return f"[{full_name}](tg://user?id={user.id})"