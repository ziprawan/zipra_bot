import traceback
import telethon, utils, base64

async def main(*args):
    event: telethon.tl.custom.message.Message = args[0]
    parser: utils.parser.Parser = args[1]
    owner: int = args[3]
    client: telethon.TelegramClient = event.client
    lang = utils.lang.Language(event)

    payload = await parser.get_args()

    if payload == None:
        return await client(
            telethon.tl.functions.messages.SendMediaRequest(
                peer = await event.get_input_chat(),
                media = telethon.tl.types.InputMediaPhoto(
                    id = telethon.tl.types.InputPhoto(
                        id = 6199740585917657401,
                        access_hash = -8701471236202862983,
                        file_reference = b'\x02D\x15\xdc\x01\x00\x00\x12\xecbAX\xa7H\xce\x1bi\xfa\xdd\xaa\xd2*Jc\x91\t\x98?+'
                    )
                ),
                message = await lang.get('report_bug_template_empty')
            )
        )
    else:
        length = utils.helper.get_length(payload)
        if length > 4000:
            return await event.respond(await lang.get('args_too_long'))
        else:
            to_encoded = f"{event.chat_id}|{event.id}"
            msg = f"{base64.b64encode(to_encoded.encode()).decode()}\n\n{payload}"
            await event.reply(await lang.get('report_bug_sent'))
            return await client.send_message(owner, msg)

async def answer_report(
    event: telethon.tl.custom.message.Message, 
    replied: telethon.tl.custom.message.Message
    ):
    if '\n' in replied.raw_text:
        splitted = replied.raw_text.split('\n')
        try:
            decoded = base64.b64decode(splitted[0])
            chat_id, message_id = decoded.decode().split("|")
            to_reply = event.raw_text
            entities = event.entities
            client: telethon.TelegramClient = event.client

            return await client.send_message(
                entity = await client.get_input_entity(int(chat_id)),
                message = to_reply,
                reply_to = int(message_id),
                parse_mode = None,
                formatting_entities = entities
            )
        except:
            print(traceback.format_exc())
    else:
        pass