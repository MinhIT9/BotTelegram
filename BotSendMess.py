from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Danh sách ID của các channel mà bạn muốn gửi tin nhắn đến.
# Bạn cần thay thế `@your_channel_1`, `@your_channel_2`, ... 
# với tên hoặc ID thực sự của các channel của bạn.
TOKEN_BOT = '6500285460:AAEm_dyWXxszfm0T3DJmMFrRV4Ez6M8jQcg'
CHANNELS = ['@chanws1', '@chan9090s']

async def forward_to_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Lấy tin nhắn từ người dùng
    user_message = update.message.text
    
    # Gửi tin nhắn đến tất cả các channel trong danh sách
    # for channel_id in CHANNELS:
    #     await context.bot.send_message(chat_id=channel_id, text=user_message)
    for channel_id in CHANNELS:
        # Kiểm tra loại tin nhắn và chuyển tiếp tương ứng
        if update.message.text:
            # Gửi tin nhắn văn bản
            await context.bot.send_message(chat_id=channel_id, text=update.message.text)
        elif update.message.photo:
            # Gửi ảnh, lấy ảnh có độ phân giải cao nhất
            photo = update.message.photo[-1]
            await context.bot.send_photo(chat_id=channel_id, photo=photo.file_id, caption=update.message.caption)
        elif update.message.video:
            # Gửi video
            await context.bot.send_video(chat_id=channel_id, video=update.message.video.file_id, caption=update.message.caption)


# Tạo một ứng dụng bot với token của bạn.
app = ApplicationBuilder().token(TOKEN_BOT).build()

# Thêm một MessageHandler để xử lý tất cả tin nhắn văn bản gửi đến bot
app.add_handler(MessageHandler(filters.ALL, forward_to_channels))

# Bắt đầu bot
app.run_polling()
