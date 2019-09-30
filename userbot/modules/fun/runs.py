import random

from userbot.events import register

DISABLE_RUN = False

RUNSREACTS = [
    "Runs to Thanos",
    "Runs far, far away from earth",
    "Running faster than usian bolt coz I'mma Bot",
    "Runs to Marie",
    "This Group is too cancerous to deal with.",
    "Cya bois",
    "Kys",
    "I am a mad person. Plox Ban me.",
    "I go away",
    "I am just walking off, coz me is too fat.",
    "I Fugged off!",
]


@register(outgoing=True, pattern="^.runs$")
async def runner_lol(run):
    """ Run, run, RUNNN! """
    if not DISABLE_RUN:
        index = random.randint(0, len(RUNSREACTS) - 1)
        reply_text = RUNSREACTS[index]
        await run.edit(reply_text)


@register(outgoing=True, pattern="^.disable runs$")
async def disable_runs(norun):
    """ Some people don't like running... """
    global DISABLE_RUN
    DISABLE_RUN = True
    await norun.edit("```Done!```")


@register(outgoing=True, pattern="^.enable runs$")
async def enable_runs(run):
    """ But some do! """
    global DISABLE_RUN
    DISABLE_RUN = False
    await run.edit("```Done!```")
