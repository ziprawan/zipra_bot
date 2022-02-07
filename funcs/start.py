from utils.lang import Language
from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonUrl, KeyboardButtonRow, User
from telethon.tl.custom.message import Message

async def main(*args):
    event: Message = args[0]
    parsed = args[1]
    me: User = args[2]
    sender = await event.get_sender()
    lang = Language(event)

    args = await parsed.get_options()
    if args == None or args == "start":
        if event.is_private:
            return await event.respond(
                (await lang.get("start_message_private")).format(
                    name = sender.first_name,
                    bot_name = me.first_name
                )
            )
        else:
            return await event.reply(
                await lang.get("start_message_non_private"),
                buttons = ReplyInlineMarkup(
                    rows = [KeyboardButtonRow(
                        buttons = [KeyboardButtonUrl(
                            text = await lang.get("click_here", True),
                            url = f"https://t.me/{me.username}?start=start"
                        )]
                    )]
                )
            )