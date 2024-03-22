from telegram import Update
from telegram.ext import ContextTypes
from config import CHANNELS

#set Channel
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
    if not CHANNELS:
        await update.message.reply_text("No channels have been set.")
        return
    
    message = "Current channels:\n"
    for number, channel_id in CHANNELS.items():
        message += f"Number {number}: {channel_id}\n"
    
    await update.message.reply_text(message)
