import time
PONG = "🏓 **PONG!!!**"

async def main(msg, *another):
    result = await msg.reply_text(PONG)
    waktu_awal = msg.date
    waktu_akhir = time.time()
    waktu_respon = round(waktu_akhir - waktu_awal, 3)
    return await result.edit_text(f"{PONG}\n⏱ <code>{waktu_respon}'s</code>")
