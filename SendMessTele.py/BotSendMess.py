from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from module import set_channel, show_channels, handle_message
from config import TOKEN_BOT, commands_list, update_channels, main

#Show ALL Command hiện tại BOT đang có
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Danh sách các lệnh của bot:\n\n"
    for command, description in commands_list:
        message += f"{command}: {description}\n"
    await update.message.reply_text(message)

app = ApplicationBuilder().token(TOKEN_BOT).build()

#Show all Command
app.add_handler(CommandHandler('admin', admin))

#Forward  and Edit Message
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

#Set Channel
app.add_handler(CommandHandler( "setChannel",set_channel))
#Show Channel
app.add_handler(CommandHandler('showChannel', show_channels))

app.run_polling()