from time import sleep

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^.log(?:\s+|$)([\s\S]*)")
async def log(log_text):
    """ For .log command, forwards a message
     or the command argument to the bot logs group """
    if BOTLOG:
        if log_text.reply_to_msg_id:
            reply_msg = await log_text.get_reply_message()
            await reply_msg.forward_to(BOTLOG_CHATID)
        elif log_text.pattern_match.group(1):
            user = f"#LOG / Chat ID: {log_text.chat_id}\n\n"
            textx = user + log_text.pattern_match.group(1)
            await bot.send_message(BOTLOG_CHATID, textx)
        else:
            await log_text.edit("`What am I supposed to log?`")
            return
        await log_text.edit("`Logged Successfully`")
    else:
        await log_text.edit("`This feature requires Logging to be enabled!`")
    sleep(2)
    await log_text.delete()

add_help_item(
    ".log",
    "Utilities",
    "Logs the message to the bot log group, or forwards the "
    "replied to message to the group.",
    """
    `.log (message)`
    
    Or, in response to a message
    `.log`
    """
)