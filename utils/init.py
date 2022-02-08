import dotenv, os
from telethon.sync import TelegramClient

# Load .env
if os.path.exists('.env'):
    dotenv.load_dotenv('.env')
else:
    raise ValueError(".env is missing!")

env = os.environ
api_id = env.get("API_ID", None)
api_hash = env.get("API_HASH", None)
bot_token = env.get("BOT_TOKEN", None)
owner = int(env.get("OWNER", None))

if bot_token == "" or bot_token == None:
    raise ValueError("Your Bot Token cannot be empty or None.")

# End read .env
# Initialize client
client = TelegramClient("mybot", api_id, api_hash).start(bot_token=bot_token)

with client:
    me = client.get_me()
    
