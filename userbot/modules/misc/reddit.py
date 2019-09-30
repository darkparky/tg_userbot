from userbot.events import register


@register(outgoing=True, pattern=r"\/?r\/(\S+)")
async def subreddit(r):
    sub = r.pattern_match.group(1)
    link = f"[r/{sub}](https://reddit.com/r/{sub})"
    await r.edit(link)