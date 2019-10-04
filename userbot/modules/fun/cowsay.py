from cowpy import cow


from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.(\w+)say (.*)")
async def univsaye(cowmsg):
    """ For .cowsay module, userbot wrapper for cow which says things. """
    arg = cowmsg.pattern_match.group(1).lower()
    text = cowmsg.pattern_match.group(2)

    if arg == "cow":
        arg = "default"
    if arg not in cow.COWACTERS:
        return
    cheese = cow.get_cow(arg)
    cheese = cheese()

    await cowmsg.edit(f"`{cheese.milk(text).replace('`', '´')}`")

COWACTERS = [f"`{c}`" for c in cow.COWACTERS]
add_help_item(
    ".cowsay",
    "Fun",
    "Uses [cowpy](https://github.com/jeffbuttars/cowpy) to cowsay your message.",
    f"""
    `.(variation)say (message)`
    
    Example: `.cowsay Hello world`
    
    Variations:
    {', '.join(COWACTERS)}
    """
)
