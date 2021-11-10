from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
START = """Hello, perkenalkan, namaku Zipra.

Insya Allah, bot ini akan berkembang agar bisa mengatur grup dengan mudah 👍

Kalau pengen lihat bantuan, ketik /help aja 👌"""

def main(msg, *another):
    if msg.chat.type != "private":
        msg.reply_text("O jangan disini 🗿", True,
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Klik disini lol", url="https://t.me/zipra_bot?start")]
                    ]))
    else:
        msg.reply_text(START)
