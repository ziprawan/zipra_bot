from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import requests, random, os
link_photo = [
        'https://cdn0-production-images-kly.akamaized.net/tt5Xav7-Kp0oO2pB6G8Kgup01v4=/640x853/smart/filters:quality(75):strip_icc():format(jpeg)/kly-media-production/medias/3594659/original/040089700_1633527349-ikhsan-baihaqi-pbc2wXbQYpI-unsplash.jpg', 
        'https://cdns.klimg.com/merdeka.com/i/w/news/2019/11/11/1124739/540x270/indomie-goreng-jadi-salah-satu-ramen-terlezat-di-dunia-rev-1.jpg', 
        'https://asset.kompas.com/crops/1krZIfsafldhRMvEjXCRbd2zlf8=/15x8:639x424/750x500/data/photo/2020/12/18/5fdc4b5936a6c.jpeg', 
        'https://imgsrv2.voi.id/0Aebc37hu-NXHLDaPAJlGkJzmy4BAn1jYI76GKAII-k/auto/1200/675/sm/1/bG9jYWw6Ly8vcHVibGlzaGVycy8yOTUyNi8yMDIxMDEyOTEzMDctbWFpbi5jcm9wcGVkXzE2MTE5MDA0OTMuanBn.jpg']
teks = ['a', 'b', 'c', 'd', 'e']

async def main(msg: CallbackQuery, command, args: str):
    if args == str(msg.from_user.id):
        message = msg.message
        if message.from_user == None:
            return await msg.answer("Anonymous detected +++", True)
        button = InlineKeyboardButton("Refresh", callback_data=f'/indomie {msg.from_user.id}')
        markup = InlineKeyboardMarkup([[button]])
        terpilih = random.choice(link_photo)
        tekss = random.choice(teks)
        photo = InputMediaPhoto(terpilih, tekss)
        await message.edit_media(photo, reply_markup=markup)
        if os.path.exists('indomie.jpg'):
            os.remove('indomie.jpg')
        return True
    else:
        return await msg.answer("Tombol ini bukan buat kamu lol", show_alert=True)