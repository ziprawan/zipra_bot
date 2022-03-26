from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
START = """Hello, perkenalkan, namaku {}.

Insya Allah, bot ini akan berkembang agar bisa mengatur grup dengan mudah 👍

Kalau pengen lihat bantuan, ketik /help aja 👌"""

async def main(msg: Message, cmd, args):
    me = await msg._client.get_me()
    if msg.chat.type != "private":
        uname = str(me.username)
        return await msg.reply(
            "O jangan disini 🗿",
            True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Klik disini lol", url=f"https://t.me/{uname}?start")
                    ]
                ]
                )
            )
    elif args:
        return await msg.reply(args)
    else:
        await msg.reply_text(START.format(me.first_name))
