# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway(yes, Internet). """


import re
import urllib
from datetime import datetime

import requests
import speedtest
from requests import ConnectionError
from dns.resolver import Resolver
from telethon import functions

from userbot import CMD_HELP
from userbot.events import register
from userbot.utils.helpers import parse_arguments

@register(outgoing=True, pattern=r"^.d(?:ig)? (\S+)")
async def dig_dns(dig):
    resolver = Resolver()
    host = dig.pattern_match.group(1)
    a = resolver.query(host, 'A', raise_on_no_answer=False)
    aaaa = resolver.query(host, 'AAAA', raise_on_no_answer=False)
    ns = resolver.query(host, 'NS', raise_on_no_answer=False)
    mx = resolver.query(host, 'MX', raise_on_no_answer=False)
    txt = resolver.query(host, 'TXT', raise_on_no_answer=False)

    response = "**DNS Results for %s**\n" % host
    response = response + "\n**ANSWER SECTION:**\n"
    response = response + str(a.rrset) + "\n"
    response = response + "\n**AUTHORITY SECTION:**\n"
    response = response + str(ns.rrset) + "\n"
    response = response + "\n**ADDITIONAL SECTION:**\n"
    additionals = [i for i in [mx.rrset, aaaa.rrset, txt.rrset] if i]
    response = response + '\n'.join(map(str, additionals))

    await dig.edit(response)

@register(outgoing=True, pattern=r"^.f(?:ollow)?(?: |$)(.*)?")
async def follow_url(event):
    reply_message = await event.get_reply_message()
    message_text = event.pattern_match.group(1)
    opts, message_text = parse_arguments(message_text)

    await event.edit("Fetching links...")

    urls = []
    if message_text:
        matches = re.findall(r'(https?://\S+)', message_text)
        urls.extend(list(matches))
    elif reply_message:
        matches = re.findall(r'(https?://\S+)', reply_message.text)
        urls.extend(list(matches))
    else:
        await event.edit("No URLs found :(")
        return

    base_domain = opts.get('full', False)
    await event.edit("Following links...")

    follows = []
    for url in urls:
        followed = await resolve_url(url, base_domain)
        follows.append((url, followed))

    message = []
    for follow in follows:
        message.append(f"**Original URL:** {follow[0]} \n**Followed URL:** {follow[1]}")
    
    message = '\n \n'.join(message)
    await event.edit(message, link_preview=False)

@register(outgoing=True, pattern="^.speed$")
async def speedtst(spd):
    """ For .speed command, use SpeedTest to check server speeds. """
    await spd.edit("`Running speed test . . .`")
    test = speedtest.Speedtest()

    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()

    await spd.edit("`"
                   "Started at "
                   f"{result['timestamp']} \n\n"
                   "Download "
                   f"{speed_convert(result['download'])} \n"
                   "Upload "
                   f"{speed_convert(result['upload'])} \n"
                   "Ping "
                   f"{result['ping']} \n"
                   "ISP "
                   f"{result['client']['isp']}"
                   "`")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2**10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


@register(outgoing=True, pattern="^.dc$")
async def neardc(event):
    """ For .dc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Country : `{result.country}` \n"
                     f"Nearest Datacenter : `{result.nearest_dc}` \n"
                     f"This Datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^.ping$")
async def ping(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % (duration))

async def resolve_url(url: str, base_domain: bool = True) -> str:
    """Follow all redirects and return the base domain
    Args:
        url: The url
    Returns:
        The base comain as given by urllib.parse
    """
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    if not url.startswith('http'):
        url = f'http://{url}'
    try:
        req = requests.get(url, headers=headers)
        url = req.url
    except ConnectionError:
        pass
    netloc = urllib.parse.urlparse(url).netloc
    # split up the result to only get the base domain
    # www.sitischu.com => sitischu.com
    _base_domain = netloc.split('.', maxsplit=netloc.count('.') - 1)[-1]
    if _base_domain and base_domain:
        url = _base_domain
    return url

CMD_HELP.update({
    "Network": {
        "dig":
            "Returns dns info for a domain. \n"
            "Usage: `.d(ig) (domain)`",
        "follow":
            "Follows a short url and returns it's destination. \n"
            "Usage: `.f(ollow) (url)?`",
        "speed":
            "Conduct a speed test and show the results. \n"
            "Usage: `.speed`",
        "dc":
            "Find the nearest datacenter from your server. \n"
            "Usage:`.dc`",
        "ping":
            "Show how long it takes to ping your bot. \n"
            "Usage: `.ping`"
    }
})
