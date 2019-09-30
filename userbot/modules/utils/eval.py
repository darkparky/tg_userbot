from os import remove

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register


@register(outgoing=True, pattern=r"^.eval(?: |$)([\S\s]+)")
async def evaluate(query):
    """ For .eval command, evaluates the given Python expression. """
    reply_message = await query.get_reply_message()
    if query.is_channel and not query.is_group:
        await query.edit("`Eval isn't permitted on channels`")
        return

    if query.pattern_match.group(1):
        expression = query.pattern_match.group(1)
    elif reply_message:
        expression = reply_message.text
    else:
        await query.edit("``` Give an expression to evaluate. ```")
        return

    if expression in ("userbot.session", "config.env"):
        await query.edit("`That's a dangerous operation! Not Permitted!`")
        return

    try:
        evaluation = str(eval(expression))
        if evaluation:
            if isinstance(evaluation, str):
                if len(evaluation) >= 4096:
                    file = open("output.txt", "w+")
                    file.write(evaluation)
                    file.close()
                    await query.client.send_file(
                        query.chat_id,
                        "output.txt",
                        reply_to=query.id,
                        caption="`Output too large, sending as file`",
                    )
                    remove("output.txt")
                    return
                await query.edit("**Query: **\n`"
                                 f"{expression}"
                                 "`\n**Result: **\n`"
                                 f"{evaluation}"
                                 "`")
        else:
            await query.edit("**Query: **\n`"
                             f"{expression}"
                             "`\n**Result: **\n`No Result Returned/False`")
    except Exception as err:
        await query.edit("**Query: **\n`"
                         f"{expression}"
                         "`\n**Exception: **\n"
                         f"`{err}`")

    if BOTLOG:
        await query.client.send_message(
            BOTLOG_CHATID,
            f"Eval query {expression} was executed successfully")
