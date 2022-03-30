from funcs import *
from callback import *
from utils.database import MyDatabase
import telethon

commands = {
    'start': start, 'dbg': dbg, 'ping': ping,
    'help': help, 'setlang': lang, 'eval': my_eval, 'ban': bans,
    'unban': bans, 'scope': other.scope, 'debugmode': other.debugmode,
    'report_bug': other.report_bug
}

callbacks = {
    'help': chelp, 'setlang': clang
}

async def cooldown(event: telethon.tl.custom.message.Message):
    sender_id = event._sender_id