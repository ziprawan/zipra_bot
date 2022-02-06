from pyrogram.types import Message
from utils.databases import Database
import re

async def main(msg: Message, cmd, args):
    # Initialize database
    db = Database('databases/notes.db', 'notes')

    if cmd == 'notes' or cmd == 'tags':
        return await get_tag(msg, db)
    elif cmd == 'tag':
        return await add_tag(msg, db, args)
    elif cmd == 'untag':
        return await delete_tag(msg, db, args)

async def add_tag(msg: Message, db: Database, args):
    if args == None:
        return await msg.reply("Argumen tidak cukup!\nFormat: <code>/tag #nama_tag isi_tag</code>")
    chat_id = msg.chat.id
    pattern = re.compile(r'^(#?(\w+))')
    r = pattern.search(args)
    tag_name = r[2]
    temp_content = args.replace(f'{r[1]}', '', 1)

    if msg.reply_to_message != None:
        if msg.reply_to_message.text == None:
            return await msg.reply("Untuk sementara save tag yg bermedia belum bisa.")
        content = msg.reply_to_message.text
        if temp_content != '':
            content += f'\n{temp_content}'
        
        if (await db.get_data(['name'], [tag_name])) != []:
            await db.update_data(['content'], [content], ['chat_id', 'name'], [chat_id, tag_name])
            return await msg.reply(f"Tag #{tag_name} berhasil di update!")
        else:
            await db.insert_data(['chat_id', 'content', 'name'], [chat_id, content, tag_name])
            return await msg.reply(f"Tag #{tag_name} berhasil di simpan!")
    else:
        if temp_content == '':
            return await msg.reply("Reply ke message atau tambahkan teks untuk menambahkan tag!")
        else:
            content = temp_content
            if (await db.get_data(['name'], [tag_name])) != []:
                await db.update_data(['content'], [content], ['chat_id', 'name'], [chat_id, tag_name])
                return await msg.reply(f"Tag #{tag_name} berhasil di update!")
            else:
                await db.insert_data(['chat_id', 'content', 'name'], [chat_id, content, tag_name])
                return await msg.reply(f"Tag #{tag_name} berhasil di simpan!")


async def delete_tag(msg: Message, db: Database, args):
    if args == None:
        return await msg.reply("Argumen tidak cukup!\nFormat: <code>/untag #nama_tag</code>")
    chat_id = msg.chat.id
    pattern = re.compile(r'^(#?(\w+))')
    r = pattern.search(args)
    tag_name = r[2]
    fetched_tag = await db.get_data(['chat_id', 'name'], [msg.chat.id, tag_name])
    if fetched_tag == []:
        return await msg.reply(f"Tag #{tag_name} tidak ditemukan!")
    await db.delete_data(['chat_id', 'name'], [chat_id, tag_name])
    return await msg.reply(f"Tag #{tag_name} berhasil dihapus!")


async def get_tag(msg: Message, db):
    # Create table for current group if doesn't exists
    await db.execute(f"CREATE TABLE IF NOT EXISTS notes(id INT, chat_id INT, name TEXT, content TEXT, document TEXT)")

    # Get table content
    # db.execute("SELECT * FROM notes WHERE chat_id=?", (msg.chat.id,))
    # fetched = cur.fetchall()
    fetched = await db.get_data(['chat_id'], [msg.chat.id])

    # Listing all fetched data
    if fetched == []:
        message = "There is no notes in this chat!"
    else:
        message = "Notes in this chat are:\n\n"
        for i in fetched:
            addon = f"~ <code>#{i[2]}</code>\n"
            message += addon
    
    # Send result
    await msg.reply(message, True)