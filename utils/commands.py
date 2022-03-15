from funcs import *
from callback import *

commands = {
    'start': start, 'dbg': dbg, 'ping': ping,
    'help': help, 'setlang': lang, 'eval': my_eval, 'ban': bans,
    'unban': bans, 'scope': other.scope, 'debugmode': other.debugmode
}

callbacks = {
    'help': chelp, 'setlang': clang
}