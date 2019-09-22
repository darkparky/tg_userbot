# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway(yes, Internet). """

from datetime import datetime

import speedtest
from dns.resolver import Resolver
from telethon import functions

from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.dig (\S+)")
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


@register(outgoing=True, pattern="^.nearestdc$")
async def neardc(event):
    """ For .nearestdc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Country : `{result.country}` \n"
                     f"Nearest Datacenter : `{result.nearest_dc}` \n"
                     f"This Datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^.pingme$")
async def pingme(pong):
    """ FOr .pingme command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % (duration))


CMD_HELP.update(
    {"speed": ".speed"
     "\nUsage: Conduct a speedtest and show the results."})
CMD_HELP.update({
    "nearestdc":
    ".nearestdc"
    "\nUsage: Find the nearest datacenter from your server."
})
CMD_HELP.update(
    {"pingme": ".pingme"
     "\nUsage: Show how long it takes to ping your bot."})
