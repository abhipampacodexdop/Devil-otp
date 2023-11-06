from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import users

start_message = """
**Hello {} welcome to Devil-OTP! 

• Your Gateway to Telegram Virtual Accounts! 💼✨

• Buy virtual accounts with ease and elevate your Telegram experience! 📲🔥

• Experience Telegram like never before with Ace's virtual accounts! 🌟💬

• Upgrade your messaging game with Ace's virtual accounts. 💪💎

• Step into a new era of Telegram with Ace's virtual account offerings. 🚀🔓

~ Price: ₹15 per ID/OTP only/-**
"""

start_buttons = [
  [
    InlineKeyboardButton("Purchase ID - ₹15", callback_data="purchase")
  ],
  [
    InlineKeyboardButton("Deposit funds 🏦", callback_data="deposit"),
    InlineKeyboardButton("Refer & earn 💵", callback_data="refer")
  ],
  [
    InlineKeyboardButton("Your stats 📊", callback_data="stats")
  ],
  [
    InlineKeyboardButton("Updates 📢", url="t.me/"),
    InlineKeyboardButton("Support 👥", url="t.me/Elisha_support")
  ],
]

@Client.on_message(filters.private & filters.command(["start", "help", "buy"]))
async def start_msg(c, message):
  if len(message.text)>7:
      if users.check(message.from_user.id):
        await message.reply("**You already started the bot ♦️**")
      else:
        string = message.text.split(" ", 1)[1]
        refer_user_id = string.split("-")[1]
        users.adduser(message.from_user.id, refer_user_id)
        await message.reply(f"**You're refer by {refer_user_id}**")
        refer_text = "**NEW REFER \n\n**"
        refer_text += f"**User:** {message.from_user.mention}\n"
        refer_text += f"**User ID:** {message.from_user.id}"
        await c.send_message(refer_user_id, refer_text)
      await message.reply(start_message.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(start_buttons))
  else:
     users.adduser(message.from_user.id, 5497627952)
     await message.reply(start_message.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(start_buttons))

