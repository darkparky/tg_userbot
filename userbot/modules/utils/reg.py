""" Allows !! commands to be registered """
import mimetypes
import os
import re
from datetime import datetime
from functools import reduce

from minio import ResponseError

from ..help import add_help_item
from ..dbhelper import add_command, delete_command, get_command, get_commands
from userbot import minioClient, MINIO_BUCKET, bot, MONGO
from userbot.events import register
from userbot.utils import parse_arguments


@register(outgoing=True, pattern=r"^\.reg(\s+[\S\s]+)")
async def register_command(e):
    reply_message = await e.get_reply_message()
    params = e.pattern_match.group(1)
    args, params = parse_arguments(params, ['update'])
    update = args.get('update', False)

    command, _, text = params.partition(' ')
    command, text = command, text if text else None

    await e.edit(f"Registering command `{command}`...")

    message = reply_message if reply_message else e.message
    text = reply_message.text if reply_message else text

    if message.sticker:
        sticker = {
            'id': message.sticker.id,
            'access_hash': message.sticker.access_hash
        }
        status = await add_command(command, text, sticker=sticker)
    elif message.photo:
        print(message.photo)
        photo_path = await save_file(message.photo)
        status = await add_command(command, text, photo_path)
    elif message.gif:
        gif_path = await save_file(message.gif)
        status = await add_command(command, text, gif_path)
    elif message.document:
        doc_path = await save_file(message.document)
        status = await add_command(command, text, doc_path, False, True)
    else:
        status = await add_command(command, text)

    if status:
        await e.edit(f"Registered command `{command}`", delete_in=3)
    else:
        await e.edit(f"Failed to register command `{command}`", delete_in=3)


@register(outgoing=True, pattern=r"^!!(\S+)")
async def call_registered_command(e):
    reply_message = await e.get_reply_message()
    command = e.pattern_match.group(1)
    command = await get_command(command)

    if command:
        await e.delete()
        if command.get('attachment'):
            name = command.get('attachment')
            print([o.object_name.encode('utf-8') for o in minioClient.list_objects(MINIO_BUCKET)])
            
            minioClient.fget_object(
                MINIO_BUCKET,
                name,
                f'./downloads/{name}'
            )
            
            await e.client.send_file(
                e.chat_id,
                f"./downloads/{name}",
                caption=command.get('message'),
                force_document=command.get('send_as_document'),
                reply_to=reply_message,
                link_preview=False
            )
        elif command.get('sticker'):
            # TODO
            pass
        else:
            await e.client.send_message(
                e.chat_id,
                command.get('message'),
                reply_to=reply_message,
                link_preview=False
            )


@register(outgoing=True, pattern=r"^\.unreg (\S+)")
async def unregister_command(e):
    command = e.pattern_match.group(1)

    if await delete_command(command):
        await e.edit(f"Command `{command}` unregistered", delete_in=3)
    else:
        await e.edit(f"Command `{command}` doesn't seem to exist", delete_in=3)


@register(outgoing=True, pattern=r"^\.regs$")
async def list_commands(e):
    commands = await get_commands()
    commands = [c['command'] for c in commands]

    print(commands)

    def rangify(acc, cmd):
        if re.match(r"(\S+)(\d+)", cmd):
            cmd, num = re.findall(r"(\S+)(\d+)", cmd)[0]
            if not acc.get(cmd):
                acc.update({cmd: 1})
            else:
                acc[cmd] = acc[cmd] + 1
        else:
            if not acc.get(cmd):
                acc.update({cmd: None})
        return acc

    commands = reduce(rangify, commands, {})

    numbered = [cmd for cmd in commands.items() if cmd[1]]
    numbered = '\n'.join([f"{u[0]}-{u[0]}{u[1]}" for u in numbered])

    unnumbered = [cmd[0] for cmd in commands.items() if not cmd[1]]

    message = f"""**Registered Commands**
{', '.join(unnumbered)}
    
**Sequenced**
{numbered}"""
    await e.edit(message)


async def save_file(file):
    photo = await bot.download_media(file)

    name, ext = os.path.splitext(photo)
    name = name + str(int(datetime.now().timestamp()))
    name = ''.join([name, ext])

    file_stat = os.stat(photo)
    mime = mimetypes.guess_type(photo)[0]

    try:
        with open(photo, 'rb') as file:
            minioClient.put_object(MINIO_BUCKET, name, file, file_stat.st_size, content_type=mime)
        os.remove(photo)
        return name
    except ResponseError:
        return False


add_help_item(
    ".reg",
    "Utilities",
    "Register a simple command which sends a message, "
    "photo, sticker, or file of some kind.",
    """
    With an optional file attachment of some kind
    `.reg (command) [message]`
    
    In reply to a message
    `.reg (command)`
    """
)

add_help_item(
    ".unreg",
    "Utilities",
    "Unregister (delete) a registered command.",
    """
    `.unreg (command)`
    """
)

add_help_item(
    ".regs",
    "Utilities",
    "List all registered commands.",
    """
    `.regs`
    """
)
