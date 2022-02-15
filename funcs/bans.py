from utils.helper import check_admin
from utils.lang import Language
from telethon.tl.custom.message import Message
from telethon.tl.functions.messages import SendMediaRequest
from telethon.tl.types import InputMediaDocument, InputDocument
from telethon.sync import TelegramClient

async def ban(event: Message, params: str| None):
    chat = await event.get_chat()
    client: TelegramClient = event.client

    replied = await event.get_reply_message()
    if replied == None:
        return await event.respond("Reply to user!")
    else:
        user = await replied.get_sender()

    p = await client.edit_permissions(
        chat,
        user,
        0,
        view_messages=False,
        send_messages=False
    )
    print(p)
    if p.updates != []:
        await client.delete_messages(chat, p.updates[0])
    await event.respond("Mampus, kena ban 😅👆")
    return await client(SendMediaRequest(
        peer = chat,
        media = InputMediaDocument(
            id = InputDocument(
                id=6080049489123476920, 
                access_hash=-8737819976689190729, 
                file_reference=b'\x02_U\xfe\x0e\x00\x00M\xb5b\x0b4\xf3\xbd\xebR\xa9\xf1<=\xac\x94nt\xebG\xe2\x08\xa9',
            )
        ),
        message = "Ini stiker"
    ))

async def unban(event: Message, params: str|None):
    chat = await event.get_chat()
    client: TelegramClient = event.client

    replied = await event.get_reply_message()

    if replied == None:
        return await event.reply("Reply to user")
    else:
        user = await replied.get_sender()

    p = await client.edit_permissions(
        entity = chat,
        user = user,
        until_date = 0,
        view_messages = True,
        send_messages = True
    )

async def main(*args):
    event: Message = args[0]
    parser = args[1]
    lang = Language(event)

    param = await parser.get_options()
    ca = await check_admin(event)

    if ca != True:
        return await event.reply(await lang.get('admin_error'))

    cmd = await parser.get_command()
    if cmd == "ban":
        return await ban(event, param)
    elif cmd == "unban":
        return await unban(event, param)