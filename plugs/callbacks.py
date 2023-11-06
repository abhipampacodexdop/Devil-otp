import pyqrcode, os, sys, pytz, random
from pyrogram import filters, Client
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from database import users
from . import cancel, get_stats
from .seller import *
from .start import *

a_chat = -1001867815837
bot_username = ""
back_button = [[InlineKeyboardButton("⌫", callback_data="back")]] 

async def refer_bonus(RiZoeL, user_id, amount):
  check = users.check(user_id)
  refer_ = check.refer_by
  bonus = float(float(amount) * 3/100) 
  ref = users.update_deposit(refer_, bonus)
  try:
     await RiZoeL.send_message(refer_, f"**Refer bonus 💥 \n\n ➡️ Deposit by: {user_id} \n ➡️ Amount: ₹{amount} \n ➡️ Your Commission (3%): ₹{bonus} \n ➡️ Total refer amount: ₹{ref}**")
  except:
     pass

async def get_amount(RiZoeL: Client, message: Message):
   chat = message.chat
   amount = await RiZoeL.ask(chat.id, "💲 **Share the amount of deposit \n\nMinimum deposit ₹16 or else wouldn't be added**", filters.text, timeout=300)
   if await cancel(amount):
      return "cancel"
   elif amount.text.isnumeric():
      if int(amount.text) >= 16:
         if int(int(amount.text) / 16) <= int(sess.count()):
            return int(amount.text)
         else:
            await amount.reply(f"**Sorry! Currently only {sess.count()} IDs in stock, so you can add upto ₹{int(sess.count()) * 16} only.**")
            return await get_amount(RiZoeL, message)
      else:
         await amount.reply("❗Minimum amount ₹16")
         return await get_amount(RiZoeL, message)
   else:
      await amount.reply("⚠️ Amount should be in Numbers! E.g 100")
      return await get_amount(RiZoeL, message)

async def get_ss(RiZoeL, m, amount):
   proof = await RiZoeL.ask(m.chat.id, f"💳 **Pay ₹{amount} on given QR code! and share screenshot!**", timeout=300)
   if proof.photo:
      return proof
   else:
      if await cancel(proof):
         return "cancel"
      else:
         await proof.reply("**Please share screenshot, or send /cancel to cancel the process**")
         return await get_ss(RiZoeL, m, amount)
   

async def add_fundings(RiZoeL: Client, message: Message):
   chat = message.chat
   kolkata_timezone = pytz.timezone("Asia/Kolkata")
   current_time = pytz.utc.localize(message.date).astimezone(kolkata_timezone).time()
   if 23 < current_time.hour or current_time.hour < 9:
      await RiZoeL.send_message(chat.id, "**Sorry it's sleep time! You cannot add/deposit funds between 11PM to 09AM, because Team is Off**")
      return 
   user = await RiZoeL.get_users(chat.id)
   amount = await get_amount(RiZoeL, message)
   if amount == "cancel":
      return
   hue = await RiZoeL.send_message(user.id, "wait generating QR Code...")
   s = str(f"upi://pay?pa=7887030826@paytm&pn=Devil OTP&am={amount}")
   qrname = str(chat.id)
   qrcode = pyqrcode.create(s)
   qrcode.png(qrname + '.png', scale=6)
   img = qrname + '.png'
   await RiZoeL.send_photo(
             chat.id,
             img,
             caption="**SCAN and PAY** 🧾")
   await hue.delete()
   proof = await get_ss(RiZoeL, message, amount)
   if proof == "cancel":
      return 
   logs = "**New Deposit!** \n\n"
   logs += f"by user: {user.mention} \n"
   logs += f"Amount: ₹{amount} \n"
   log_buttons = [
                  [
                  InlineKeyboardButton("Approve", callback_data=f"pay:a:{user.id}:{amount}")
                  ],
                  [
                  InlineKeyboardButton("R - SS", callback_data=f"pay:r:ss:{user.id}:{amount}"),
                  InlineKeyboardButton("R - Cont", callback_data=f"pay:r:cont:{user.id}:{amount}")
                  ],
                  ]
   await RiZoeL.send_photo(
               a_chat,
               proof.photo.file_id,
               caption=logs,
               reply_markup=InlineKeyboardMarkup(log_buttons))
   await proof.reply("**☑️ Screenshot and amount submitted to Team! Wait for approval**")
   
@Client.on_callback_query()
async def callbacks(RiZoeL: Client, callback_query: CallbackQuery):
   query = callback_query.data.lower()
   message = callback_query.message
   user = callback_query.from_user

   if query == "back":
      await callback_query.edit_message_text(start_message.format(user.mention), reply_markup=InlineKeyboardMarkup(start_buttons))

   elif query == "purchase":
      if int(sess.count()) != 0:
         if int(users.check(user.id).deposit) > 15:
            await message.delete()
            await start_purchase(RiZoeL, message)
         else:
            await callback_query.edit_message_text(f"**Sorry!! You don't have enough funds! Your Deposits: ₹{users.check(user.id).deposit} \n\nKindly add funds!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Deposit funds 🏦", callback_data="deposit")]])) 
      else:
         await callback_query.edit_message_text("**Opps sorry 😐 0 IDs in stock, try again later!**")

   elif query == "refer":
      await callback_query.edit_message_text(f"**refer with your friends and earn 3% commission on per deposits \n\n Your refer link:** `https://t.me/{bot_username}?start=Devil-{user.id}`")
   
   elif query == "deposit":
      await message.delete()
      await add_fundings(RiZoeL, message)
   
   elif query == "stats":
      await callback_query.edit_message_text(get_stats(user.id), reply_markup=InlineKeyboardMarkup(back_button))

   elif query.startswith("pay"):
      que = query.split(':')
      if que[1] == "a":
         amount = users.update_deposit(int(que[2]), int(que[3]))
         await refer_bonus(RiZoeL, int(que[2]), int(que[3]))
         await RiZoeL.send_message(que[2], f"**Your Request for ₹{que[3]} has been approved \n\nTotal amount/deposit: ₹{amount}**")
         await message.delete()
         await RiZoeL.send_message(message.chat.id, f"**Approved deposit** ✓ \n\nuser: {que[2]} \nAmount: ₹{amount}")
       
      elif que[1] == "r":    
         if que[2] == "ss":
            u = await RiZoeL.get_users(que[3])
            msg = await RiZoeL.send_photo(u.id, message.photo.file_id)
            await msg.reply(f"**Your deposit request for ₹{que[4]} has been rejected** \nReason: Screenshot invalid!")
            await message.delete()
            await RiZoeL.send_message(message.chat.id, f"**Reject deposit** ✓ \n\nuser: {que[3]} \nAmonut: ₹{que[4]}")
            proof = await RiZoeL.ask(u.id, f"**Pay ₹{que[4]} and please share valid screenshot!**", filters.photo, timeout=600)
            logs = "**Resend Screenshot of Deposit!** \n\n"
            logs += f"by user: {u.mention} \n"
            logs += f"Amount: ₹{que[4]} \n"
            log_buttons = [
                  [
                  InlineKeyboardButton("Approve", callback_data=f"pay:a:{u.id}:{que[4]}")
                  ],
                  [
                  InlineKeyboardButton("R - SS", callback_data=f"pay:r:ss:{u.id}:{que[4]}"),
                  #InlineKeyboardButton("R - Pay", callback_data=f"pay:r:p:{user.id}:{que[4]}"),
                  InlineKeyboardButton("R - Cont", callback_data=f"pay:r:cont:{u.id}:{que[4]}")
                  ],
                  ]
            await RiZoeL.send_photo(
               a_chat,
               proof.photo.file_id,
               caption=logs,
               reply_markup=InlineKeyboardMarkup(log_buttons))
            await proof.reply("**☑️ Screenshot and amount submitted to Team! Wait for approval**")
         elif que[2] == "cont":
            u = await RiZoeL.get_users(que[3])
            await RiZoeL.send_message(u.id, f"**⚠️ Something went wrong! Your request for ₹{que[4]} has been rejected by Team! please contact us. Support**")
            await message.delete()
            await RiZoeL.send_message(message.chat.id, f"**Approved deposit** ✓ \n\nuser: {que[3]} \nAmonut: ₹{que[4]}")
