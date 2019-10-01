from asyncio.subprocess import create_subprocess_shell as asyncrunapp, PIPE as asyncPIPE

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern="^.sysd$")
async def sysdetails(sysd):
    """ For .sysd command, get system info using neofetch. """
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            neo = "neofetch --stdout"
            fetch = await asyncrunapp(
                neo,
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) \
                     + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("Please install neofetch before using this", delete_in=3)

add_help_item(
    ".sysd",
    "Misc",
    "Gets system information using neofetch.",
    "`.sysd`"
)
