from search_engine_parser import GoogleSearch

from userbot import BOTLOG, BOTLOG_CHATID
from userbot.events import register
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^.google(?: |$)(.*)")
async def gsearch(q_event):
    """ For .google command, do a Google search. """
    reply_message = await q_event.get_reply_message()
    query = q_event.pattern_match.group(1)
    opts, query = parse_arguments(query, ['page', 'limit'])

    page = opts.get('page', 1)
    gsearch = GoogleSearch()

    query = query or reply_message.text
    gresults = gsearch.search(query, page)

    msg = ""
    limit = opts.get('limit', 5)
    for i in range(limit):
        try:
            title = gresults["titles"][i]
            link = gresults["links"][i]
            desc = gresults["descriptions"][i]
            msg += f"[{title}]({link}) \n"
            msg += f"`{desc}`\n\n"
        except IndexError:
            break
    await q_event.edit("**Search Query:**\n`" + query + "`\n\n**Results:**\n" +
                       msg,
                       link_preview=False)
    if BOTLOG:
        await q_event.client.send_message(
            BOTLOG_CHATID,
            "Google Search query `" + query + "` was executed successfully",
        )