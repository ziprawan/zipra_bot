import logging
from utils.lang import Language
from utils.parser import Parser
from telethon.tl.custom.message import Message
from telethon.tl.types import (
    ReplyInlineMarkup, 
    KeyboardButtonUrl, 
    KeyboardButtonRow, 
    User
)

async def main(*args):
    logging.debug("[StartHandler] ")
    event: Message = args[0]
    parsed = args[1]
    me: User = args[2]
    owner: int = args[3]
    sender = await event.get_sender()
    lang = Language(event)

    params = await parsed.get_options()
    prsr = Parser(me.username, f'/{params}')
    cmd = await prsr.get_command()
    link_arg = cmd if params else 'start'
    if not event.is_private:
        return await event.reply(
            (await lang.get('non_private_error')),
            buttons = ReplyInlineMarkup(
                [KeyboardButtonRow([
                    KeyboardButtonUrl(
                        text = await lang.get('click_here', True),
                        url = f"https://t.me/{me.username}?start={link_arg}"
                    )
                ])]
            )
        )
    else:
        if params == None or params == "start":
            return await event.respond(
                (await lang.get("start_message_private")).format(
                    name = sender.first_name,
                    bot_name = me.first_name
                )
            )
        else:
            from utils.commands import commands
            if cmd in commands:
                return await commands[cmd].main(event, prsr, me, owner)
            else:
                return await event.respond(f'Command {cmd} not found')