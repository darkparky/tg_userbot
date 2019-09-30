import re
from importlib import import_module

from userbot.events import register


@register(outgoing=True, pattern="^.hash ([a-zA-z0-9]+)(?:\s+(.*))?")
async def gethash(hash_q):
    """ For .hash command, find the md5,
        sha1, sha256, sha512 of the string. """
    reply_message = await hash_q.get_reply_message()
    algo_name = hash_q.pattern_match.group(1)
    hashtxt = hash_q.pattern_match.group(2) or reply_message.text

    if not re.match(r"(md[245]|sha1|sha256|ripemd)", algo_name):
        await hash_q.reply(f"Unknown hashing function `{algo_name}`. See `.help hash` for info.")
        return
    else:
        algo_name = algo_name.upper()

    algo = import_module('Crypto.Hash.' + algo_name).new()
    algo.update(hashtxt.encode('utf-8'))
    output = algo.hexdigest()

    await hash_q.reply(f'{algo_name}: `{output}`')