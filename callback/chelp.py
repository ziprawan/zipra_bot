import logging
from telethon.events.callbackquery import CallbackQuery
from utils.helper import ol_generator
from utils.init import owner
from telethon import __version__
from telethon.tl.types import (
    InputMessageEntityMentionName,
    InputUser,
    InputUserSelf,
    KeyboardButtonCallback,
    KeyboardButtonRow,
    MessageEntityCode,
    ReplyInlineMarkup,
)
from utils.lang import Language


async def main(*args):
    logging.debug("[HelpCallback] Setting up variables")
    event: CallbackQuery.Event = args[0]
    parser = args[1]
    lang = Language(event)
    sender = await event.get_sender()
    me = await event.client.get_me()
    owner_info = await event.client.get_entity(owner)

    logging.debug("[HelpCallback] Parsing arguments")
    param = parser.args
    entities = []
    logging.debug("[HelpCallback] Found arguments: %s" % param)

    if param == "home":
        logging.debug("[HelpCallback] Home page")
        help_message = await lang.get("help_message")
        version = f"v{__version__}"

        # vars
        variables = ['name', 'bot_name', 'version']
        results = [sender.first_name, me.first_name, version]
        offs, lens = ol_generator(help_message, variables, results)

        logging.debug("[HelpCallback] Edit help message")
        return await event.edit(
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
    elif param == "pnt":
        logging.debug("[HelpCallback] Getting message of privacy and terms")
        msg = await lang.get('privacy_and_terms')
    elif param == 'about':
        logging.debug("[HelpCallback] Getting message of about")
        msg = await lang.get('about_me')
        msg = msg.format(
            id = me.id,
            name = me.first_name,
            uname = f'@{me.username}',
            oid = owner_info.id,
            oname = owner_info.first_name,
            ouname = f'@{owner_info.username}'
        )
    elif param == 'usage':
        logging.debug("[HelpCallback] Getting message of usage")
        msg = "None"

    logging.debug("[HelpCallback] Editing message")
    await event.edit(
        msg,
        parse_mode = None,
        buttons = ReplyInlineMarkup([KeyboardButtonRow([KeyboardButtonCallback(await lang.get('home', True), f'help_{sender.id}_home'.encode())])]),
        formatting_entities = entities
    )