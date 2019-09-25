import io

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^!screenshot$")
async def screenshot(e):
    open_and_send(e, './userbot/images/screenshot.jpg')


async def open_and_send(e, filepath):
    await e.delete()
    
    reply_message = await e.get_reply_message()
    file = io.open(filepath, 'rb')
    
    await e.client.send_file(
        e.chat_id,
        file,
        caption="Please don't send screenshots of code. Use a pastebin like del.dog.",
        reply_to=reply_message)
    file.close()