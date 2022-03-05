from funcs import *
from callback import *

commands = {
    'start': start, 'dbg': dbg, 'ping': ping,
    'help': help, 'setlang': lang, 'eval': my_eval, 'ban': bans,
    'unban': bans
}

callbacks = {
    'help': chelp, 'setlang': clang
}