import pytesseract, time, os
from PIL import Image
from pyrogram.types import Message

def remove(path):
    if os.path.exists(path):
        return os.remove(path)

def main(msg: Message, *another):
    ups = str(round(time.time()))[-6:-1]
    if msg.reply_to_message == None:
        msg.reply("Reply ke suatu pesan agar ku baca")
    else:
        if msg.reply_to_message.photo != None:
            path = msg.reply_to_message.download()
            result = pytesseract.image_to_string(path)
            msg.reply(f'Hasil OCR:\n\n{result}')
            remove(path)
        elif msg.reply_to_message.sticker != None:
            path = msg.reply_to_message.download()
            filename = f'ocr-temp{ups}.png'
            img = Image.open(path)
            img.save(filename, 'png')
            result = pytesseract.image_to_string(filename)
            msg.reply(f'Hasil OCR:\n\n{result}')
            remove(path)
            remove(filename)
        else:
            return msg.reply("Maaf, OCR hanya mendukung photo dan sticker")
            
