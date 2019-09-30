from userbot.events import register

PENIS_TEMPLATE = """
🍆🍆
🍆🍆🍆
  🍆🍆🍆
    🍆🍆🍆
     🍆🍆🍆
       🍆🍆🍆
        🍆🍆🍆
         🍆🍆🍆
          🍆🍆🍆
          🍆🍆🍆
      🍆🍆🍆🍆
 🍆🍆🍆🍆🍆🍆
 🍆🍆🍆  🍆🍆🍆
    🍆🍆       🍆🍆
"""


@register(outgoing=True, pattern=r"^.(?:penis|dick)\s?(.)?")
async def emoji_penis(e):
    emoji = e.pattern_match.group(1)

    await e.edit("Dickifying...")
    message = PENIS_TEMPLATE
    if emoji:
        message = message.replace('🍆', emoji)

    await e.edit(message)