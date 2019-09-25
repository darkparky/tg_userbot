import re
import time

from github.Repository import Repository
from github.NamedUser import NamedUser
from github.GithubException import UnknownObjectException

from userbot import github
from userbot.events import register
from userbot.utils.helpers import parse_arguments,  extract_urls

GITHUB_REPO_RE = r"(?:github\.com\/|[\s]|^)([\w\d_\-.]+)\/([\w\d_\-.]+)"

@register(outgoing=True, pattern=r"^.gh\s?([\S\s]+)?")
async def github_info(e):
    if not github:
        await e.edit("Github information has not been set up", delete_in=3)
        return
    
    reply_message = await e.get_reply_message()
    
    repo = e.pattern_match.group(1)
    if repo:
        args, repo = parse_arguments(repo)
        repo = repo.strip()
    else:
        args = {}

    repo = repo or reply_message.text
    repos = re.findall(GITHUB_REPO_RE, repo)
    if repos:
        await e.edit(f"Fetching information for {len(repos)} repo(s)...")
        message_parts = []
        invalid_repos = []
        for user, repo in repos:
            try:
                r: Repository = github.get_repo(f"{user}/{repo}")
                message = await build_repo_message(r, args)
                message_parts.append(message)
            except UnknownObjectException:
                invalid_repos.append(f"{user}/{repo}")
                pass

        message = ""
        if message_parts:
            message += '\n\n'.join(message_parts)
        if invalid_repos:
            message += "**Invalid repos:**"
            for repo in invalid_repos:
                message += str(repo)

        await e.edit(message)
    else:
        await e.edit("No GitHub repos found", delete_in=3)
        return

async def build_repo_message(repo, args):
    show_general = args.get('general', True)
    show_owner = args.get('owner', False)
    show_all = args.get('all', False)

    if show_all:
        show_general = True
        show_owner = True

    message = f"**[{repo.name}]({repo.html_url})** \n"
    
    if show_general:
        message += f"  **general** \n"
        message += f"    id: {repo.id} \n"
        message += f"    full name: {repo.full_name} \n"
        message += f"    stars: {repo.stargazers_count} \n"
        message += f"    watchers: {repo.watchers_count} \n"
        message += f"    forks: {repo.forks_count} \n"
        message += f"    language: {repo.language} \n"
        message += f"    is fork: {repo.fork} \n"
        message += f"    issues: {repo.open_issues} \n"

    if show_owner:
        owner: NamedUser = github.get_user(repo.owner.login)
        bio = str(owner.bio)[:50] + (str(owner.bio)[50:] and '..')

        message += f"  **owner** \n"
        message += f"    id: {owner.id} \n"
        message += f"    login: [{owner.login}]({owner.url}) \n"
        message += f"    name: {owner.name} \n"
        message += f"    bio: {bio} \n"
        message += f"    company: {owner.company} \n"
        message += f"    email: {owner.email} \n"
        message += f"    followers: {owner.followers} \n"
        message += f"    following: {owner.following} \n"
        message += f"    repos: {owner.public_repos} \n"

    return message
