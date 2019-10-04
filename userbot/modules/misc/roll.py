import random
import re

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^.roll\s+(.*)")
async def roll_20(e):
    params = e.pattern_match.group(1)
    patterns = re.split(r"\s+", params)

    rolls = {}
    print(patterns)
    for pattern in patterns:
        count, sides = re.search(r"([0-9]+)[Dd]([0-9]+)", pattern).groups()
        count, sides = (int(count), int(sides))
        results = []
        for i in range(count):
            roll = random.randrange(1, sides + 1)
            results.append(roll)
        rolls.update({sides: results})

    grand_total = 0
    message = ""
    for roll in rolls.items():
        total = sum(roll[1])
        grand_total += total

        message += f"**d{roll[0]}:** "
        message += ', '.join(map(str, roll[1]))
        message += f" = {total} \n"

    message += f"**total:** {grand_total}"
    await e.edit(message)


add_help_item(
    ".roll",
    "Misc",
    "Roll tabletop dice in Telegram.",
    """
    `.roll (die1) (die2) ... (dieN)`
    
    Example:
    `.roll 2d4 3d6 4d8 1d20`
    """
)