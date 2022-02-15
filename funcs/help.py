from utils.lang import Language
from utils.helper import ol_generator
from telethon import __version__
from telethon.tl.custom.message import Message
from telethon.tl.types import (
    InputMessageEntityMentionName,
    InputUser,
    InputUserSelf,
    KeyboardButtonCallback,
    KeyboardButtonRow,
    KeyboardButtonUrl,
    MessageEntityCode,
    ReplyInlineMarkup,
    User
)

async def main(*args):
    event: Message = args[0]
    params = await args[1].get_options()
    me: User = args[2]
    lang = Language(event)
    sender = await event.get_sender()

    if not event.is_private:
        return await event.reply(
            (await lang.get('non_private_error')),
            buttons = ReplyInlineMarkup(
                [KeyboardButtonRow([
                    KeyboardButtonUrl(
                        text = await lang.get('click_here', True),
                        url = f"https://t.me/{me.username}?start=help"
                    )
                ])]
            )
        )
    else:
        if params != None:
            return await event.respond(f"Menu {params} is still in development")

        help_message = await lang.get("help_message")
        version = f"v{__version__}"

        # vars
        variables = ['name', 'bot_name', 'version']
        results = [sender.first_name, me.first_name, version]
        offs, lens = ol_generator(help_message, variables, results)

        return await event.respond(
            help_message.format(
                name = sender.first_name,
                bot_name = me.first_name,
                version = version
            ),
            formatting_entities = [
                InputMessageEntityMentionName(
                    offset = offs[0],
                    length = lens[0],
                    user_id = InputUser(
                        sender.id,
                        sender.access_hash
                    )
                ),
                InputMessageEntityMentionName(
                    offset = offs[1],
                    length = lens[1],
                    user_id = InputUserSelf()
                ),
                MessageEntityCode(
                    offset = offs[2],
                    length = lens[2],
                )
            ],
            buttons = ReplyInlineMarkup(
                rows = [KeyboardButtonRow(
                    buttons = [KeyboardButtonCallback(
                        text = await lang.get('about_me', True),
                        data = f'help_{sender.id}_about'.encode()
                    ),
                    KeyboardButtonCallback(
                        text = await lang.get('usage', True),
                        data = f'help_{sender.id}_usage'.encode()
                    )]
                ), KeyboardButtonRow(
                    buttons = [KeyboardButtonCallback(
                        text = await lang.get('privacy_terms', True),
                        data = f'help_{sender.id}_pnt'.encode()
                    )]
                )]
            )
        )