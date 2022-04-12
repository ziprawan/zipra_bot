import asyncio

from telethon.tl.custom.message import Message
from telethon import functions, types
from utils.parser import Parser


async def main(*args):
    event: Message = args[0]
    parser: Parser = args[1]
    param = parser.get_args()
    if param.raw_text is not None:
        param.cut(1)
        param = param.splitted[0]
    else:
        param = ""
    client = event.client

    if event.reply_to_msg_id:
        reply: Message = await event.get_reply_message()
        user = reply.sender_id
        sender = await reply.get_sender()
        name = sender.first_name if hasattr(sender, 'first_name') else sender.title
        msg = f"This is {name}'s profile photos sir. :D"
    else:
        msg = "This is your profile photos sir. :D"
        user = event.sender_id

    result: types.photos.Photos = await client(functions.photos.GetUserPhotosRequest(
        user_id=await client.get_input_entity(user),
        offset=0,
        max_id=0,
        limit=80 if param == "aggressive" else 10
    ))

    if len(result.photos) < 1:
        return await event.reply("Lol, I can't find any photos for you.")

    medias = []
    count = len(result.photos)
    photos = result.photos

    for i in range(count):
        medias.append(types.InputSingleMedia(
            media=types.InputMediaPhoto(
                id=types.InputPhoto(
                    id=photos[i].id,
                    access_hash=photos[i].access_hash,
                    file_reference=photos[i].file_reference
                )
            ),
            message=msg if i + 1 == count else "",
        ))
        if len(medias) == 10 or i >= count - 1:
            await client(functions.messages.SendMultiMediaRequest(
                peer=await event.get_input_chat(),
                multi_media=medias
            ))
            await asyncio.sleep(3)
            medias.clear()
