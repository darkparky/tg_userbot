from requests import get

from ..help import add_help_item
from userbot import CURRENCY_API
from userbot.events import register


@register(outgoing=True, pattern=r"^.cr (\S*) ?(\S*) ?(\S*)")
async def currency(cconvert):
    """ For .cr command, convert amount, from, to. """
    amount = cconvert.pattern_match.group(1)
    currency_from = cconvert.pattern_match.group(3).upper()
    currency_to = cconvert.pattern_match.group(2).upper()
    data = get(
        f"https://free.currconv.com/api/v7/convert?apiKey={CURRENCY_API}&q={currency_from}_{currency_to}&compact=ultra"
    ).json()
    result = data[f'{currency_from}_{currency_to}']
    result = float(amount) / float(result)
    result = round(result, 5)
    await cconvert.edit(
        f"{amount} {currency_to} is:\n`{result} {currency_from}`")

add_help_item(
    ".cr",
    "Misc",
    "Convert currencies.",
    """
    `.cr (amount) (from) (to)`
    """
)
