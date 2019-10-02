from ..help import add_help_item
from userbot.events import register


@register(pattern="^!!windows")
async def windows_interjection(e):
    reply_message = await e.get_reply_message()
    await e.respond(
        'I’d just like to interject for a moment. What you’re referring to as Windows, is in fact, NSA/Windows, or as I’ve recently taken to calling it, NSA plus Windows. Windows is not an operating system unto itself, but rather another component of a fully functioning NSA system made useful by the Windows corelibs, shell utilities and vital system components comprising a full OS as defined by General James Robert Clapper. Many computer users run a modified version of the Windows system every day, without realizing it. Through a peculiar turn of events, the version of NSA/Windows which is widely used today is often called “Windows”, and many of its users are not aware that it is basically the NSA/Windows system, developed by the NSA. There really is a Windows, and these people are using it, but it is just a part of the NSA system they use. Windows is the kernel: the program in the system that allocates the machine’s resources to the other NSA programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Windows is normally used in combination with the NSA operating system: the whole system is basically NSA with Windows added, or NSA/Windows. All the so-called “Windows” versions are really distributions of NSA/Windows.',
        reply_to=reply_message)
    await e.delete()

add_help_item(
    "!!windows",
    "Meta",
    "Displays a windows interjection.",
    "`!!windows`"
)
