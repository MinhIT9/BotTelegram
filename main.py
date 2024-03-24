from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers_command import set_channel, show_channels, admin, start
from handlers_message import handle_message
from bot_config import TOKEN_BOT

app = ApplicationBuilder().token(TOKEN_BOT).build()

#Show all Command
app.add_handler(CommandHandler('admin', admin))
app.add_handler(CommandHandler('start', start))

#Forward  and Edit Message
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

#Set Channels
app.add_handler(CommandHandler( "setChannel",set_channel))
#Show Channel
app.add_handler(CommandHandler('showChannel', show_channels))

print("***** BOT khởi động thành công *****")

app.run_polling()

