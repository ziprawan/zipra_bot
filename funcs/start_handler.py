from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
START = """Hello, perkenalkan, namaku Zipra.

Insya Allah, bot ini akan berkembang agar bisa mengatur grup dengan mudah 👍

Kalau pengen lihat bantuan, ketik /help aja 👌"""

async def main(msg: Message, *another):
    if msg.chat.type != "private":
        me = await msg._client.get_me()
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
    else:
        await msg.reply_text(START)
