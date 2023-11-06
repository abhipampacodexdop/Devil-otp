
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from database import users, sess

Devs = [5497627952]

@Client.on_message(filters.user(Devs) & filters.command(["give"]))
async def give_deposit(RiZoeL: Client, message: Message):
   txt = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 1)
   if len(txt) == 2:
      try:
         user = await RiZoeL.get_users(txt[0])
      except Exception as eor:
         await message.reply(str(eor))
         return
      amount = int(txt[1])
      if not users.check(user.id):
         users.adduser(user.id)
      yeah = users.update_deposit(user.id, amount)
      await message.reply(f"Given {amount} to {user.mention}, Total Amount: {yeah}")
   else:
      await message.reply("please gime user ID or username and amount")

@Client.on_message(filters.user(Devs) & filters.command(["take"]))
async def take_deposit(RiZoeL: Client, message: Message):
   txt = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 1)
   if len(txt) == 2:
      try:
         user = await RiZoeL.get_users(txt[0])
      except Exception as eor:
         await message.reply(str(eor))
         return
      amount = int(txt[1])
      if int(users.check(user.id).deposit) < int(amount):
         await message.reply(f"Sorry! user have only ₹{users.check(user.id).deposit} deposit, you cannot take more than ₹{users.check(user.id).deposit}")
         return
      yeah = users.take_deposit(user.id, amount)
      await message.reply(f"taken {amount} to {user.mention}, Total Amount: {yeah}")
   else:
      await message.reply("please gime user ID or username and amount")

@Client.on_message(filters.user(Devs) & filters.command(["remove"]))
async def remove_id(RiZoeL: Client, message: Message):
   txt = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 1)
   if len(txt) == 1:
      sess.remove(txt[0])
      await message.reply("Done!")

@Client.on_message(filters.user(Devs) & filters.command(["broadcast"]))
async def broadcast_(RiZoeL: Client, message: Message):
   hue = await message.reply("passing....")
   replied = message.reply_to_message
   a = 0
   if replied:
      for i in users.get_all_users():
         try:
            await replied.copy(i.user_id)
            a += 1
         except Exception as e:
            print(e)
      await hue.edit(f"**Done sent to {a} users**")
   else:
      await message.reply("please reply to message!")

def get_bot_stats():
   stats = "**Ace Stats ♦️** \n\n**"
   stats += f"**Total Users: {users.count()} \n"
   stats += f"**Total Users: {sess.count()} \n"
   stats += f"**IDs in stock: {sellers.count()} \n"
   return stats
    
@Client.on_message(filters.user(Devs) & filters.command(["stats"]))
async def get_all_stats(RiZoeL: Client, message: Message):
   wb = await message.reply("**Fetching....**")
   try:
      txt = "".join(message.text.split(maxsplit=1)[1:]).split(" ", 1)
   except Exception:
      txt = None
   if txt:
      try:
         user = await RiZoeL.get_users(txt[0])
         buyer = users.check(user.id)
         seller = sellers.check(user.id)
         if buyer:
            stats = f"**{user.mention}'s Stats** \n\n"
            stats += f"**🆔 User ID: {user_id}** \n"
            stats += f"**🛒 IDs Purchased: {buyer.orders}** \n"
            stats += f"**💳 Deposits Funds: ₹{buyer.deposit}** \n"
         else:
            stats = get_bot_stats()
      except Exception:
         stats = get_bot_stats()
   else:
      stats = get_bot_stats()
   await wb.edit_text(stats)