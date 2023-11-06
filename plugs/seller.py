import random, re, asyncio
from pyrogram import Client, filters
from database import sess, users
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

DB_CHAT = -1001738802770 

API_LIST = [
  '4014305 b0cb9e17b2b8bcde3be7161c8bfa6013',
  '28124597 7d71ada2c2b74ed53cc1b5ad829b5277',
  '3147700 e660ea4d20e70a3897aa8cf3a6dc60af',
  '18405415 65a8e3ad64aee6e570d73c02638bc6bf',
  '4487418 3a4aaa8e7e20a071667813226cb45564',
]

def get_api():
  a = random.choice(API_LIST)
  api = a.split(' ')
  return api[0], api[1]

async def get_data(RiZoeL, id):
  msg = await RiZoeL.get_messages(DB_CHAT, id)
  txt = msg.text.split(" ")
  return txt[0], txt[1]


async def fetchotp(client):
   try:
      async for x in client.get_chat_history(777000, 1):
         o = x.text.split(' ')[2]
         otp = o.split(".")[0]
         return int(otp), x.id
   except Exception as eor:
      print(eor)
      return "null", "null"

async def check_login(client, mid):
   async for i in client.get_chat_history(777000, 1):
      if int(i.id) > int(mid) and i.text.startswith("New"):
          y = x.text.split("\n\n")[1]
          return str(y)
      else:
          return "null"

async def get_id(RiZoeL, m):
  chat = m.chat 
  try:
     rows = sess.get_data()
     key = random.choice(rows)
     id = int(key.id)
  except Exception:
     key = random.choice(sess.get_list())
     id = int(key)
  session, number = await get_data(RiZoeL, id)
  aid, ahash = get_api()
  client = Client(f'{number}00', api_id=aid, api_hash=ahash, session_string=session)
  try:
     await client.start()
     await asyncio.sleep(1)
     await client.stop()
     return id
  except Exception as eor:
     #await RiZoeL.send_message(chat.id, "oops an error in login! trying with new ID!!")
     hm = sess.check(id)
     await RiZoeL.send_message(hm.user_id, f"**Hey there!** An user try to purchase ID which's seller is you. I'm facing and error, so please re-login your telegram id \n ID's phone no: {number}")
     sess.remove(id)
     sellers.less_id(hm.user_id)
     print(str(eor))
     return await get_id(RiZoeL, m)

async def start_purchase(RiZoeL, message):
  chat = message.chat
  hue = await RiZoeL.send_message(chat.id, "fetching ids................")
  id = await get_id(RiZoeL, message)
  await hue.edit_text("lets start....")
  _, number = await get_data(RiZoeL, id)
  await RiZoeL.send_message(
     chat.id,
     f"**Phone NO:  `{number}`  (tap to copy) \n\nLogin given phone number and click on 'Get OTP' button for OTP** \n\n__Once you click on 'get OTP' client will start and price of OTP charge from your deposits!__",
     reply_markup=InlineKeyboardMarkup(
       [
          [
             InlineKeyboardButton("Get OTP 🔑", callback_data=f"sell:otp:{id}")
          ],
       ]
     ),
     )

@Client.on_callback_query(filters.regex("sell"), group=0)
async def sell_callbacks(RiZoeL: Client, callback_query: CallbackQuery):
   message = callback_query.message
   chat = message.chat
   user = callback_query.from_user
   query = callback_query.data.split(":")

   if query[1] == "otp":
      id = int(query[2])
      await message.edit_text("starting ID.......")
      session, number = await get_data(RiZoeL, id)
      aid, ahash = get_api()
      client = Client(f'{number}-{id}', api_id=aid, api_hash=ahash, session_string=session)
      await client.start()
      await message.edit_text("fetching otp.......")      
      otp, mid = await fetchotp(client)
      if otp == "null":
        await message.edit("**Error! please try again!**")
        return
      await client.stop()
      remain = users.charge(user.id, 15)
      sess.remove(query[2])
      otp_text = "**Devil OTP!** \n\n"
      otp_text += f"**OTP for Phone No: {number} is**\n\n **OTP>>**   `{otp}`\n\n"
      otp_text += f"**-> Charged ₹15 for OTP remaining balance ₹{remain}** \n\n"
      otp_text += f"**#NOTE:** terminate all sessions and re-edit your profile!"
      await message.delete()
      await RiZoeL.send_message(
        chat.id, 
        otp_text,
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton("Fetch OTP again 🔄", callback_data=f"sell:eotp:{id}"),
              InlineKeyboardButton("New/Next No. ⏭️", callback_data=f"purchase")
            ],
          ]
        )
      )
      await RiZoeL.send_message('Xenvil_xd', f"**OTP Sold** \n\n Phone No: {number} \n Buyer: {user.id}")
      
   elif query[1] == 'eotp':
      id = int(query[2])
      await message.edit_text("starting ID.......")
      session, number = await get_data(RiZoeL, id)
      aid, ahash = get_api()
      client = Client(f'{number}-{id}', api_id=aid, api_hash=ahash, session_string=session)
      await client.start()
      await message.edit_text("fetching otp.......")
      otp, mid = await fetchotp(client)
      if otp == "null":
        await message.edit("**Error! please try again!**", 
                          reply_markup=InlineKeyboardMarkup(
                          [
                          [
                             InlineKeyboardButton("Fetch OTP again 🔄", callback_data=f"sell:otp:{id}")
                          ]
                          ])
             )
        return
      await message.delete()
      await client.stop()
      await RiZoeL.send_message(
        chat.id, 
        f"**OTP for Phone No: {number} is**\n\n **OTP>>**   `{otp}` \n **If Two Step then password is**: `TeamAce`",
        reply_markup=InlineKeyboardMarkup(
          [
            [
              InlineKeyboardButton("Fetch OTP again 🔄", callback_data=f"sell:eotp:{id}"),
              #InlineKeyboardButton("Login - NO ⛔", callback_data=f"sell:no:{id}:{mid}")
            #],
            #[
              InlineKeyboardButton("New/Next No. ⏭️", callback_data=f"purchase")
            ],
          ]
        )
      )
