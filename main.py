import pyroaddon, os, sys
from database import users
from pyrogram import Client, idle
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

print("[INFO]: Defining client......")

TOKEN = "6406215075:AAEC4gTWnmEdmNfTb1kBkDoSyZahBCgQZ-Q"

RiZoeL = Client(
    'Devil-Bot',
    api_id=28124597,
    api_hash="7d71ada2c2b74ed53cc1b5ad829b5277",
    bot_token=TOKEN,
    plugins=dict(root="plugs")
)
print("[INFO]: Got client!")

def Start():
    print("[INFO]: Starting Client!")
    try:
        RiZoeL.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("[INFO]: API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("[INFO]: Bot TOKEN is not valid.")
    try:
       uname = RiZoeL.get_me().username
       print(f"[INFO]: @{uname} is now running!")
    except:
       print("[INFO]: Bot is now running!")

    print("Bot started successfully!")
    idle()
    RiZoeL.stop()
    print("Bot stopped.")


if __name__ == "__main__":
    Start()
