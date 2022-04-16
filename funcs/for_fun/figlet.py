import pyfiglet
import telethon
from utils.parser import Parser
from utils.init import me
from utils.helper import get_length


async def main(*args):
    event: telethon.tl.custom.message.Message = args[0]
    parser: Parser = args[1]

    text = parser.get_args().raw_text

    if text is None:
        return await event.reply("Give text!")
    else:
        figletted = pyfiglet.figlet_format(text).rstrip()
        msg = "Figlet result:\n" + figletted
        return await event.reply(
            message = msg,
            formatting_entities = [telethon.tl.types.MessageEntityCode(
                offset = 15,
                length = get_length(figletted)
            )]
        )