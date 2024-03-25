# handlers_command.py
from telegram import Update, Bot
from telegram.ext import ContextTypes
from bot_config import CHANNELS, commands_list, update_channels, CHANNEL_API, TOKEN_BOT
from API import set_or_update_channel

bot = Bot(token=TOKEN_BOT)
        
#Show Channel
async def show_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_channels()

    # Sau khi đảm bảo CHANNELS đã được cập nhật, hiển thị nó.
    if CHANNELS:
        message_text = "Current Channels:\n"
        for number, info in CHANNELS.items():
            channel_id = info['id']
            channel_name = info['name']
            message_text += f"No: {number}: {channel_id} - {channel_name}\n"  # Hiển thị cả ID và tên kênh
        await update.message.reply_text(message_text)
        print("GET command showChannel Success!!")
    else:
        await update.message.reply_text("No channels to display or failed to update channels.")
        
#Set Channel
async def set_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if len(args) == 2:  # Yêu cầu chỉ có 2 tham số: channel_number và channel_id
        channel_number = args[0]
        channel_id = args[1]  # ID kênh

        try:
            # Lấy thông tin kênh từ Telegram
            chat = await bot.get_chat(channel_id)
            channel_name = chat.title  # Tên của kênh

            # Gọi hàm set_or_update_channel và xử lý kết quả
            result, error = await set_or_update_channel(CHANNEL_API, channel_number, channel_id, channel_name)
            if error:
                await update.message.reply_text(f"Error updating channel: {error}")
            else:
                await update.message.reply_text(f"Channel {channel_number} has been set/updated with ID {channel_id} and name \"{channel_name}\"")
        except Exception as e:
            await update.message.reply_text(f"Failed to fetch channel info or update channel: {str(e)}")
    else:
        await update.message.reply_text("Usage: /setchannel <number> <channel_id>")
        
        
#Show ALL Command
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Danh sách các lệnh của bot:\n\n"
    for command, description in commands_list:
        message += f"{command}: {description}\n"
    await update.message.reply_text(message)
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = "Chào mừng bạn đến với trợ lý xinh gái của Tu Tiên Giới nè! iu iu ❤️"
    await update.message.reply_text(message)