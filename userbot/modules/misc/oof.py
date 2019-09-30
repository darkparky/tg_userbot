from userbot.events import register


@register(outgoing=True, pattern="^([Oo]of)$")
async def Oof(e):
    t = e.pattern_match.group(1)
    for _ in range(15):
        t = t[:-1] + "of"
        await e.edit(t)
