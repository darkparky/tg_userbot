from os import remove

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register


@register(outgoing=True, pattern=r"^\.eval(?:\s+|$)([\S\s]+)")
async def evaluate(e):
    """ For .eval command, evaluates the given Python expression. """
    reply = await e.get_reply()
    if e.is_channel and not e.is_group:
        await e.edit("`Eval isn't permitted on channels`")
        return

    if e.pattern_match.group(1):
        expression = e.pattern_match.group(1)
    elif reply:
        expression = reply.text
    else:
        await e.edit("``` Give an expression to evaluate. ```")
        return

    if expression in ("userbot.session", "config.env"):
        await e.edit("`That's a dangerous operation! Not Permitted!`")
        return

    try:
        evaluation = str(eval(expression))
        if evaluation:
            if isinstance(evaluation, str):
                if len(evaluation) >= 4096:
                    file = open("output.txt", "w+")
                    file.write(evaluation)
                    file.close()
                    await e.client.send_file(
                        e.chat_id,
                        "output.txt",
                        reply_to=e.id,
                        caption="`Output too large, sending as file`",
                    )
                    remove("output.txt")
                    return
                await e.edit("**Query: **\n`"
                             f"{expression}"
                             "`\n**Result: **\n`"
                             f"{evaluation}"
                             "`")
        else:
            await e.edit("**Query: **\n`"
                         f"{expression}"
                         "`\n**Result: **\n`No Result Returned/False`")
    except Exception as err:
        await e.edit("**Query: **\n`"
                     f"{expression}"
                     "`\n**Exception: **\n"
                     f"`{err}`")

    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID,
            f"Eval query {expression} was executed successfully")


add_help_item(
    ".eval",
    "Utilities",
    "Evaluates a small Python expression using `eval()`.",
    """
    `.eval (expression)`
    
    Or, in response to a message
    `.eval`
    """
)
