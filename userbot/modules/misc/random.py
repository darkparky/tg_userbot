from random import randint

from userbot.events import register


@register(outgoing=True, pattern="^.rand(?:om)? (.*)")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = items.pattern_match.group(1).split()

    if len(itemo) < 2:
        await items.edit("`2 or more items are required! Check "
                         ".help random for more info.`")
        return

    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")
