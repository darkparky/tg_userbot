import hashlib
import re
from asyncio import sleep
from io import BytesIO

from telethon.tl.functions.users import GetFullUserRequest

from userbot.utils.tgdoc import *
from userbot.events import register
from userbot.modules.dbhelper import (add_profile_pic_hash,
                                      remove_profile_pic_hash,
                                      get_profile_pic_hash)
from userbot.utils import get_user_from_event, parse_arguments, make_mention

REDFLAG_WORDS = [
    'bitcoin', 'crypto', 'forex', 'invest',
    'sex', 'eth', 'model',
]


@register(outgoing=True, pattern=r"^\.spamscan$")
async def spamscan(e):
    """ Scan every user in the current chat and match
    them against the spam algorithm. """
    await e.edit("**Scanning for potential spammers, this may take a while...**")

    users = {}
    total = 0
    async for user in e.client.iter_participants(e.chat, aggressive=True):
        user_full = await e.client(GetFullUserRequest(user.id))
        score = await score_user(e, user_full)

        score_total = sum([i for i in score.values()])
        if score_total >= 5:
            users.update({user_full.user.id: score})

        total += 1
        print(f"Scanned {total} so far")
        # if total % 500 == 0:
        #     await sleep(5)

    output = Section(Bold("Scan Results"))
    if users:
        for item in users.items():
            user_id, score = item
            user_full = await e.client(GetFullUserRequest(user_id))
            score_total = sum([i for i in score.values()])
            output.items.append(KeyValueItem(String(make_mention(user_full.user)),
                                             Bold(str(score_total))))
    else:
        output.items.append(String("No potential spammers found"))

    await e.edit(str(output))


@register(outgoing=True, pattern=r"^\.spamscan classify (spam|ham)(\s+[\S\s]+|$)")
async def spamscan_classify(e):
    """ Feed the algorithm by classifying a user either
    as spam or ham """
    category = e.pattern_match.group(1)
    args, user = parse_arguments(e.pattern_match.group(2), ['forward'])

    args['forward'] = args.get('forward', True)
    args['user'] = user

    replied_user = await get_user_from_event(e, **args)

    if category == "spam":
        hashes = await gather_profile_pic_hashes(e, replied_user.user)
        for md5 in hashes:
            await add_profile_pic_hash(md5, True)
        await e.edit(f"**Classified {make_mention(replied_user.user)} as spam**")
    elif category == "ham":
        await e.delete()


@register(outgoing=True, pattern=r"^\.spamscan test(\s+[\S\s]+|$)")
async def spamscan_test(e):
    """ Test a single user against the spamscan algorithm """
    args, user = parse_arguments(e.pattern_match.group(1), ['forward'])

    args['forward'] = args.get('forward', True)
    args['user'] = user

    replied_user = await get_user_from_event(e, **args)
    score = await score_user(e, replied_user)
    score_total = sum([i for i in score.values()])

    output = f"Spam score for {make_mention(replied_user.user)}: **{score_total}**\n\n"

    if score_total > 0:
        output += "**Reasons:**\n"

    for reason in score.keys():
        output += f"{reason}\n"

    await e.edit(output)


async def score_user(event, userfull):
    """ Give a user a spam score based on several factors """
    user = userfull.user

    # Everyone starts with a score of 0. A lower score indicates
    # a lower chance of being a spammer. A higher score
    # indicates the opposite.
    score = {}

    # First we'll check their profile pics against registered
    # hashes that we know are spam
    hashes = await gather_profile_pic_hashes(event, user)
    total_hashes = len(hashes)
    matching_hashes = 0
    for md5 in hashes:
        match = await get_profile_pic_hash(md5)
        if match:
            matching_hashes += 1

    # No profile pic is a +2
    if total_hashes == 0:
        score.update({'no profile pic': 2})

    if matching_hashes > 0:
        # If the number of matching hashes is greater than or equal
        # to half of the total hashes we give them a +5. This is
        # basically a guarantee.
        if (total_hashes / matching_hashes) >= (total_hashes / 2):
            score.update({f'blacklisted photos ({total_hashes}/{matching_hashes})': 5})

        # Otherwise we increase their score by 3 because they still
        # have matching hashes.
        else:
            score.update({f'blacklisted photos ({total_hashes}/{matching_hashes})': 3})

    # Lots of spammers try and look normal by having a normal(ish)
    # first and last name. A first AND last name with no special
    # characters is a good indicator. This is a +1.
    if ((user.first_name and re.match(r"[a-zA-Z0-9\s_]+", user.first_name)) or
            (user.last_name and re.match(r"[a-zA-Z0-9\s_]+", user.last_name))):
        score.update({'alphanum first and last name': 1})

    if user.first_name and user.last_name:
        # Another thing spammers seem to have is very predictable names.
        # These come in many forms like one uppercase name and one
        # lowercase, all upper or lower, or having one name be
        # numeric. Either way they generally have a first
        # name and a last name.
        if user.first_name.isupper() or user.first_name.islower():
            score.update({'first upper last lower': 3})
        elif user.last_name.isupper() or user.last_name.islower():
            score.update({'first lower last upper': 3})
        elif user.first_name.islower() and user.last_name.islower():
            # This appears less bot like than all upper
            score.update({'lowercase name': 2})
        elif user.first_name.isupper() and user.last_name.isupper():
            score.update({'uppercase name': 3})
        elif user.first_name.isnumeric() or user.last_name.isnumeric():
            score.update({'numeric name': 2})

    # Another popular thing is bots with japanese, chinese, cyrillic,
    # and arabic names. A full match here is worth +3.
    if (user.first_name and is_cjk(user.first_name) or
            (user.last_name and is_cjk(user.last_name))):
        score.update({'ch/jp name': 3})
    elif (user.first_name and is_arabic(user.first_name) or
            (user.last_name and is_arabic(user.last_name))):
        score.update({'arabic name': 3})
    elif (user.first_name and is_cyrillic(user.first_name) or
            (user.last_name and is_cyrillic(user.last_name))):
        # Cyrillic names are more common, so we'll drop the score here.
        score.update({'cyrillic name': 2})

    # A username ending in numbers is a +1
    if user.username and re.match(r".*[0-9]+$", user.username):
        score.update(({'sequential username': 1}))

    if userfull.about:
        # Check the bio for red flag words. Each one of these is a +3.
        total_red_flags = 0
        for word in REDFLAG_WORDS:
            if word in userfull.about.lower():
                total_red_flags += 1
        if total_red_flags > 0:
            score.update({f'red flag words x{total_red_flags}': total_red_flags * 3})

    # No bio is also an indicator worth an extra 2 points
    else:
        score.update({'no bio': 2})

    return score


def is_cjk(string):
    return unicode_block_match(string, [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215),
                                        (63744, 64255), (65072, 65103), (65381, 65500),
                                        (131072, 196607)])


def is_arabic(string):
    return unicode_block_match(string, [(1536, 1791), (1792, 1871)])


def is_cyrillic(string):
    return unicode_block_match(string, [(1024, 1279)])


def unicode_block_match(string, block):
    re.sub(r"\s+", "", string)
    for char in string:
        if not any([start <= ord(char) <= end for start, end in block]):
            return False
    return True


async def gather_profile_pic_hashes(event, user):
    hashes = []
    async for photo in event.client.iter_profile_photos(user, limit=10):
        io = BytesIO()
        await event.client.download_media(photo, io)
        md5 = hashlib.md5(io.getvalue())
        hashes.append(md5.hexdigest())
    return hashes
