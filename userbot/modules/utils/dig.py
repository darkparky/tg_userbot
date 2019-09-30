from dns.resolver import Resolver

from userbot.events import register


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