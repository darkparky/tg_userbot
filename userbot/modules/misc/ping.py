from datetime import datetime

from userbot.events import register


@register(outgoing=True, pattern="^.ping$")
async def ping(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % duration)
