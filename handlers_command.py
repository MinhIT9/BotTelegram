# handlers_command.py
from telegram import Update
from telegram.ext import ContextTypes
from bot_config import CHANNELS, commands_list, update_channels

#Set Channel
async def set_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) >= 2:
        channel_number = args[0]
        channel_id = ' '.join(args[1:])  # Cho phép ID kênh chứa dấu cách
        CHANNELS[channel_number] = channel_id
        await update.message.reply_text(f"Channel {channel_number} has been set to {channel_id}")
    else:
        await update.message.reply_text("Usage: /setchannel <number> <channel_id>")
        
#Show Channel
async def show_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    await update_channels()

    # Sau khi đảm bảo CHANNELS đã được cập nhật, hiển thị nó.
    if CHANNELS:
        message_text = "Current Channels:\n"
        for number, channel_id in CHANNELS.items():
            message_text += f"Number {number}: {channel_id}\n"
        await update.message.reply_text(message_text)
        print("GET command showChannel Success!!")
    else:
        await update.message.reply_text("No channels to display or failed to update channels.")

#Show ALL Command hiện tại BOT đang có
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Danh sách các lệnh của bot:\n\n"
    for command, description in commands_list:
        message += f"{command}: {description}\n"
    await update.message.reply_text(message)
    