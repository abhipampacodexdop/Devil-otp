from database import users, sellers

def get_stats(user_id):
  check = users.check(user_id)
  stats = "**Your Stats 📊** \n\n"
  stats += f"**🆔 Your ID: {user_id}** \n"
  stats += f"**🛒 IDs Purchased: {check.orders}** \n"
  stats += f"**💳 Deposits Funds: ₹{check.deposit}**"
  return stats

async def cancel(msg):
  if msg.text:
     if "/cancel" in msg.text:
        await msg.reply("**Process cancelled ❌**")
        return True
     elif "/restart" in msg.text:
        await msg.reply("**Process cancelled ❌**")
        return True
     elif msg.text.startswith("/"):
        await msg.reply("**Process cancelled ❌**")
        return True
  else:
     return False
