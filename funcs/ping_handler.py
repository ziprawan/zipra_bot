import time
PONG = "🏓 **PONG!!!**"

def main(msg, *another):
    result = msg.reply_text(PONG)
    waktu_awal = msg.date
    waktu_akhir = time.time()
    waktu_respon = round(waktu_akhir - waktu_awal, 3)
    return result.edit_text(f"{PONG}\n⏱ <code>{waktu_respon}'s</code>")
