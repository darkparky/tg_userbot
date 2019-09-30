from userbot.events import register


@register(outgoing=True, pattern="^.lfy(?: |$)(.*)",)
async def let_me_google_that_for_you(lmgtfy):
    if not lmgtfy.text[0].isalpha() and lmgtfy.text[0] not in ("/", "#", "@", "!"):
        textx = await lmgtfy.get_reply_message()
        query = lmgtfy.text
        if query[5:]:
            query = str(query[5:])
        elif textx:
            query = textx
            query = query.message
        reply_text = 'Hmm... [Let Me Google That For You](http://lmgtfy.com/?s=g&iie=1&q=' + query.replace(" ", "+") + ")"
        await lmgtfy.edit(reply_text)