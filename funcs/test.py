from pyrogram.types import Message
import asyncio

async def my_progress(current, total, *args):
    msg = args[0]
    print(current, total)
    await asyncio.sleep(1)
    downloaded = f"{current * 100 / total:.1f}"
    try:
        downloaded = float(downloaded)
    except:
        await msg._client.stop_transmission()
        return await msg.edit("Something went wrong!")
    if downloaded < 100:
        return await msg.edit(f"{msg.text} {downloaded}%")
    else:
        return await msg.edit(f"Finished!")

async def main(msg: Message, cmd, args):
    if args:
        oh = await msg.reply("Uploading...")
        await msg.reply_document(args, progress=my_progress, progress_args=(oh,))
        return await oh.edit("Dun!")
    if not msg.reply_to_message:
        return await msg.reply("Testing doang, coba reply ke media", True)
    rtm = msg.reply_to_message
    if not rtm.media:
        return await msg.reply("Testing doang, coba reply ke media", True)
    prog: Message = await msg.reply("Downloading...", True)
    downl = await rtm.download(
        progress = my_progress,
        progress_args = (prog,)
    )
    return await prog.edit(f"Finished!\nPath: {downl}")