""" Allows !! commands to be registered """
import mimetypes
import os
from datetime import datetime

from minio import ResponseError

from ..help import add_help_item
from ..dbhelper import add_command, delete_command, get_command, get_commands
from userbot import minioClient, MINIO_BUCKET, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^.reg (\S+)([\S\s]+|$)")
async def register_command(e):
    reply_message = await e.get_reply_message()
    command = e.pattern_match.group(1)
    text = e.pattern_match.group(2)

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
    command = e.pattern_match.group(1)
    command = await get_command(command)

    if command:
        await e.delete()
        if command.get('attachment'):
            name = command.get('attachment')
            attachment = minioClient.fget_object(
                MINIO_BUCKET,
                name,
                f'./downloads/{name}'
            )
            await e.client.send_file(
                e.chat_id,
                f"./downloads/{name}",
                caption=command.get('message'),
                force_document=command.get('send_as_document')
            )
        elif command.get('sticker'):
            # TODO
            pass
        else:
            await e.client.send_message(
                e.chat_id,
                command.get('message')
            )


@register(outgoing=True, pattern=r"^.unreg (\S+)")
async def unregister_command(e):
    command = e.pattern_match.group(1)

    if await delete_command(command):
        await e.edit(f"Command `{command}` unregistered", delete_in=3)
    else:
        await e.edit(f"Command `{command}` doesn't seem to exist", delete_in=3)


@register(outgoing=True, pattern=r"^.regs$")
async def list_commands(e):
    commands = await get_commands()
    commands = [f"`{c['command']}`" for c in commands]
    message = "**Commands** \n" + '  '.join(commands)
    await e.edit(message)


async def save_file(file):
    photo = await bot.download_media(file)

    name, ext = os.path.splitext(photo)
    name = name + str(int(datetime.now().timestamp()))
    name = ''.join([name, ext])

    file_stat = os.stat(photo)
    mime = mimetypes.guess_type(photo)[0]

    try:
        print(name, file_stat.st_size, mime)
        with open(photo, 'rb') as file:
            minioClient.put_object(MINIO_BUCKET, name, file, file_stat.st_size, content_type=mime)
        return name
    except ResponseError:
        return False
