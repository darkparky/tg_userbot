import urllib.parse

from ..help import add_help_item
from userbot.events import register
from userbot.utils import parse_arguments

PROVIDERS = {
    "lmgtfy": {
        "message": "Let me Google that for you",
        "source": "https://lmgtfy.com/?s=g&iie=1&q={}"
    },
    "google": {
        "message": "Why don't you try Google?",
        "source": "https://google.com/search?q={}&sourceid=yourmom"
    },
    "ddg": {
        "message": "Let's check Duck Duck Go",
        "source": "https://duckduckgo.com/?q={}"
    },
    "bing": {
        "message": "Why don't you give Bing a go?",
        "source": "https://www.bing.com/search?q={}"
    },
    "ecosia": {
        "message": "Try searching and planting a tree or two",
        "source": "https://www.ecosia.org/search?q={}"
    }
}


@register(outgoing=True, pattern=r"^\.lfy(\s+[\S\s]+|$)", )
async def let_me_google_that_for_you(e):
    providers = list(PROVIDERS.keys())
    params = e.pattern_match.group(1) or ""
    args, message = parse_arguments(params, providers)

    provider = PROVIDERS['lmgtfy']
    for p in providers:
        if args.get(p):
            provider = PROVIDERS[p]

    reply_message = await e.get_reply_message()
    query = message if message else reply_message.text
    query = urllib.parse.quote_plus(query)

    message = provider['message']
    url = provider['source'].format(query)

    await e.edit(f"[{message}]({url})")


add_help_item(
    ".lfy",
    "Misc",
    "Uses lmgtfy or a number of other providers to "
    "provide a passive aggressive suggestion to use "
    "a search engine. Provider defaults to lmgtfy.",
    f"""
    `.lfy [provider] (query)`
    
    Or, in reply to a message
    `.lfy [provider]`
    
    Examples:
    `.lfy .google how to use python`
    `.lfy why am I so stupid`
       
    Providers:
    {', '.join([f"`{provider}`" for provider in PROVIDERS.keys()])}
    """
)
