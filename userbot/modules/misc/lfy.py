from ..help import add_help_item
from userbot.events import register
from userbot.utils import parse_arguments

PROVIDERS = {
    "lmgtfy": {
        "message": "let me Google that for you.",
        "source": "http://lmgtfy.com/?s=g&iie=1&q={}"
    },
    "google": {
        "message": "why don't you try Google?",
        "source": "https://google.com/search?q={}&sourceid=yourmom"
    },
    "ddg": {
        "message": "let's check Duck Duck Go.",
        "source": "https://duckduckgo.com/?q={}"
    },
    "bing": {
        "message": "why don't you give Bing a go?",
        "source": "https://www.bing.com/search?q={}"
    }
}


@register(outgoing=True, pattern=r"^.lfy([\S\s]+|$)", )
async def let_me_google_that_for_you(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        params = e.pattern_match.group(1) or ""
        args, message = parse_arguments(params, ['source'])

        source = args.get('source', 'lmgtfy')
        if not PROVIDERS.get(source):
            source = 'lmgtfy'
        provider = PROVIDERS[source]

        reply_message = await e.get_reply_message()
        query = message if message else reply_message.text

        reply_text = f"Hmm, [{provider['message']}]({provider['source'].format(query)})"
        await e.edit(reply_text)

add_help_item(
    ".lfy",
    "Misc",
    "Let Me Google That for You",
    """
    `.lfy (query)`
    
    Or, in reply to a message
    `.lfy`
    """
)
