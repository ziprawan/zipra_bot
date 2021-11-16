import logging

# Logging purposes
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
logging.info("Importing Modules....")

import pyrogram
import time
from utils import *
from funcs import *
from callback import *
from utils import clean_service

# Some variables
owner = 1923158017
bot = pyrogram.Client("mybot", workers=20)
bot.start()
me = bot.get_me()
user_command = {
    'start': start_handler, 'ping': ping_handler, 'pong': ping_handler,
    'json': json_handler, 'kickme': kbm_handler, 'indomie': indomie_handler
}
admin_command = {
    'del': del_handler, 'pin': pins_handler, 'unpin': pins_handler,
    'mute': kbm_handler
}
creator_command = {
     'cleanservice': clean_service
}
owner_command = {
     'getpp': getpp_handler, 'ocr': ocr_handler, 'restart': restart
}
callbacks = {
    'indomie': indomie_callback, 'kick': kick_callback, 'kickgajadi': kick_callback
}

# Callback handlers
@bot.on_callback_query()
def callback_query_handler(bot, msg: pyrogram.types.CallbackQuery):
    try:
        # print(f'{msg.from_user.username} mengklik tombol di {msg.message.chat.title}, id message: {msg.message.message_id}')
        parser = commands.parser(me.username, msg.data)
        # print(msg.data)
        command = parser.get_command()
        args = parser.get_options(command)
        if command in callbacks:
            callbacks[command].main(msg, bot, command, args)
    except Exception as e:
        bot.send_message(owner, str(e))

# Service message handlers
@bot.on_message(pyrogram.filters.service)
def service_filter(_, msg):
    return services.main(msg)

# Message handler including edited message
@bot.on_message()
def message_handlers(bot, msg: pyrogram.types.Message):
    try:
        # Teks pesan
        if msg.text != None:
            text = msg.text
        elif msg.caption != None:
            text = msg.caption
        else:
            text = None

        # User id
        if msg.from_user != None:
            userid = msg.from_user.id
        else:
            userid = None
        parser = commands.parser(me.username, text)
        command = parser.get_command()
        args = parser.get_options(command)
        if command == None:
            return
        if command in user_command:
            return user_command[command].main(msg, bot, command, args)
        
        if msg.chat.type == 'private':
            return None
        ca = check_admin.main(msg)
        if command in admin_command:
            if ca == 'administrator' or ca == 'creator':
                return admin_command[command].main(msg, bot, command, args)
            else:
                return msg.reply("Kamu harus menjadi admin atau creator grup ini!")
        elif command in creator_command:
            if ca == 'creator':
                return creator_command[command].main(msg, bot, command, args)
            else:
                return msg.reply("Kamu harus menjadi creator grup ini!")
        elif command in owner_command:
            if userid == owner:
                return owner_command[command].main(msg, bot, command, args)
        else:
            pass
    except pyrogram.errors.FloodWait as e:
        time.sleep(e.x)
    except pyrogram.errors.ChatAdminRequired as e:
        msg.reply(e, True)
    except UnicodeDecodeError:
        pass
    except Exception as e:
        return bot.send_message(owner, str(e))
    

pyrogram.idle()
bot.stop()
