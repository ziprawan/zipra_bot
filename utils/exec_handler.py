# import contextlib, sys
# from io import StringIO

# @contextlib.contextmanager
# def stdoutIO(stdout=None):
#     old = sys.stdout
#     if stdout is None:
#         stdout = StringIO()
#     sys.stdout = stdout
#     yield stdout
#     sys.stdout = old

# async def main(msg, cmd, args):
#     print(args)
#     if args == None:
#         return await msg.reply("No args!")
#     with stdoutIO() as s:
#         try:
#             exec(args)
#             return await msg.reply(str(s.getvalue()))
#         except Exception as e:
#             print(f"Error dengan alasan: {e}")
    

import sys, io, traceback

async def main(msg, cmd, args):
    if args == None:
        return await msg.reply("No args!")
    bot = msg._client
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(args, bot, msg)
    except:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    print(stdout)
    print(stderr)
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = None
    
    try:
        final_output = f"{evaluation.strip()}"
        if len(final_output) > 4096:
            with io.BytesIO(str.encode(final_output)) as outfile:
                outfile.name = "eval_result.txt"
                return await msg.reply_document(outfile)
        return await msg.reply(final_output, parse_mode=None)
    except Exception as e:
        print(e)

async def aexec(code, bot, msg):
    exec(
        "async def __aexec(bot, msg): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](bot, msg)