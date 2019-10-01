from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^.sd ([0-9]+) ([\S\s]+)")
async def selfdestruct(destroy):
    """ For .sd command, make self-destructable messages. """
    seconds = int(destroy.pattern_match.group(1))
    text = str(destroy.pattern_match.group(2))
    await destroy.edit(text, delete_in=seconds)

add_help_item(
    ".sd",
    "Misc",
    "Makes the message self destruct in a given "
    "number of seconds.",
    "`.sd (seconds) (content)`"
)
