import logging
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
    logging.debug("[HelpHandler] Setting the required variables")
    event: Message = args[0]
    logging.debug("[HelpHandler] Parsing options")
    params = await args[1].get_args()
    me: User = args[2]
    lang = Language(event)
    logging.debug("[HelpHandler] Call event.get_sender")
    sender = await event.get_sender()

    logging.info("[HelpHandler] Checking chat type")
    if not event.is_private:
        logging.info("[HelpHandler] Chat type is not private")
        logging.info("[HelpHandler] Not replying help message")
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
        logging.info("[HelpHandler] Chat type is private")
        logging.info("[HelpHandler] Sending help message")
        if params != None:
            logging.warn(f"[HelpHandler] Someone trying accessing help with param: {params}")
            return await event.respond(f"Menu {params} is still in development")

        logging.debug("Getting help_message string and telethon version")
        help_message = await lang.get("help_message")
        version = f"v{__version__}"

        logging.debug("[HelpHandler] Setting up variables for formatting_entities")
        # vars
        variables = ['name', 'bot_name', 'version']
        results = [sender.first_name, me.first_name, version]
        offs, lens = ol_generator(help_message, variables, results)

        logging.debug("[HelpHandler] Sending message with custom formatting_entities")
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