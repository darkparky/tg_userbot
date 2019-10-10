import re
from importlib import import_module

from ..help import add_help_item
from userbot.events import register
from userbot.utils.tgdoc import *

ALGORITHMS = [
    "md2", "md4", "md5", "sha224", "sha256", "sha384",
    "sha512", "ripemd"
]


@register(outgoing=True, pattern=r"^\.hash ([a-zA-z0-9]+)(?:\s+(.*))?")
async def gethash(hash_q):
    """ For .hash command, find the md5,
        sha1, sha256, sha512 of the string. """
    reply_message = await hash_q.get_reply_message()
    algo_name = hash_q.pattern_match.group(1)
    hashtxt = hash_q.pattern_match.group(2) or reply_message.text

    if algo_name not in ALGORITHMS:
        await hash_q.reply(f"Unknown hashing function `{algo_name}`. See `.help hash` for info.")
        return
    else:
        algo_name = algo_name.upper()

    algo = import_module('Crypto.Hash.' + algo_name).new()
    algo.update(hashtxt.encode('utf-8'))
    output = algo.hexdigest()

    response = Section(
        SubSection(Bold("Input:"), Code(hashtxt), indent=0),
        SubSection(Bold(f"Output ({algo_name.upper()}):"), Code(output), indent=0),
        indent=0,
        spacing=2
    )

    await hash_q.edit(str(response))


add_help_item(
    ".hash",
    "Misc",
    "Hash the supplied string with a specific hashing algorithm.",
    f"""
    `.hash (algo) (string)`
    
    **Valid algorithms:**
    {', '.join([f"`{algo}`" for algo in ALGORITHMS])}
    """
)
