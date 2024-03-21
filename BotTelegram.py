from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '6500285460:AAEm_dyWXxszfm0T3DJmMFrRV4Ez6M8jQcg'
CHANNEL_MAIN = '@Chan223a' # Kênh chính
CHANNELS_FORWARD = ['@chanws1', '@chan9090s','@Chan223a','-2133340256'] # Danh sách kênh để chuyển tiếp

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Xin chào: {update.effective_user.first_name}')

async def forward_to_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:  # Kiểm tra xem update.message có tồn tại
        try:
            for channel in CHANNELS_FORWARD:
                await context.bot.forward_message(chat_id=channel, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Update does not contain a message.")
        

app = ApplicationBuilder().token(TOKEN).build()

# Handler cho lệnh /hello
app.add_handler(CommandHandler("hello", hello))

# Handler này sẽ bắt và chuyển tiếp mọi tin nhắn đến các kênh khác
# Bạn cần xác định rõ điều kiện để không chuyển tiếp mọi thứ một cách mù quáng, đây chỉ là ví dụ
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_channels))

app.run_polling()
