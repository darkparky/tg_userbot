# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing hash and encode/decode commands. """

import re
from importlib import import_module

import pybase64
from Crypto.Hash import MD5

from userbot import CMD_HELP
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

@register(outgoing=True, pattern="^.b64 (en|de)(?:\s+(.*))?")
async def endecrypt(query):
    """ For .b64 command, find the base64 encoding of the given string. """
    reply_message = await query.get_reply_message()
    text = query.pattern_match.group(2) or reply_message.text
    if query.pattern_match.group(1) == "en":
        lething = str(pybase64.b64encode(bytes(text, "utf-8")))[2:]
        await query.reply("Encoded: `" + lething[:-1] + "`")
    else:
        lething = str( pybase64.b64decode(bytes(text, "utf-8"), validate=True))[2:]
        await query.reply("Decoded: `" + lething[:-1] + "`")


CMD_HELP.update({
    "b64": 
    "Find the base64 encoding of the given string or replied message. \n"
    "Usage: `b64 (en|de) (text)?`"
    })

CMD_HELP.update({
    "hash":
    "Hash a string using one of the following algorithms: "
    "md2, md4, md5, sha1, sha256, ripemd \n"
    "Usage: 1hash (algo) (text)?`"
})
