from funcs import *
from callback import *

commands = {
    'start': start, 'dbg': dbg, 'ping': ping,
    'help': help, 'setlang': lang, 'eval': execc, 'ban': bans
}

callbacks = {
    'help': chelp, 'setlang': clang
}