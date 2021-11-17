import pytesseract, time, os
from PIL import Image
from pyrogram.types import Message

async def remove(path):
    if os.path.exists(path):
        return os.remove(path)

async def main(msg: Message, *another):
    ups = str(round(time.time()))[-6:-1]
    if msg.reply_to_message == None:
        return await msg.reply("Reply ke suatu pesan agar ku baca")
    else:
        if msg.reply_to_message.photo != None:
            path = await msg.reply_to_message.download()
            result = pytesseract.image_to_string(path)
            await msg.reply(f'Hasil OCR:\n\n{result}')
            await remove(path)
        elif msg.reply_to_message.sticker != None:
            path = await msg.reply_to_message.download()
            filename = f'ocr-temp{ups}.png'
            img = Image.open(path)
            img.save(filename, 'png')
            result = pytesseract.image_to_string(filename)
            await msg.reply(f'Hasil OCR:\n\n{result}')
            await remove(path)
            await remove(filename)
        else:
            return await msg.reply("Maaf, OCR hanya mendukung photo dan sticker")
            
