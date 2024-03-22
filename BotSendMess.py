from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import re

TOKEN_BOT = '6500285460:AAEm_dyWXxszfm0T3DJmMFrRV4Ez6M8jQcg'
CHANNELS = {
    '1': '@Chan223a',
    '2': '@chanws1',
    '3': '@chan9090s',
    '4': '-1002133340256'
}

async def forward_to_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Kiểm tra xem có tin nhắn để xử lý không
    if update.message is None:
        return  # Không có tin nhắn để xử lý, thoát khỏi hàm

    # Khởi tạo biến để lưu trữ nội dung tin nhắn hoặc chú thích (caption)
    content = update.message.text or update.message.caption

    # Tìm kiếm kí hiệu đánh dấu và số theo sau trong nội dung
    matches = re.findall(r'#(\d+)', content if content else '')
    target_channels = [CHANNELS.get(digit) for match in matches for digit in match if CHANNELS.get(digit)]

    # Gửi tin nhắn đến các channel tương ứng
    for channel_id in target_channels:
        if update.message.text:
            # Nếu có nội dung văn bản, gửi như tin nhắn văn bản
            message_to_send = re.sub(r'#\d+', '', content).strip()
            await context.bot.send_message(chat_id=channel_id, text=message_to_send)
        elif update.message.photo:
            # Nếu là hình ảnh, gửi kèm chú thích (nếu có)
            photo = update.message.photo[-1].file_id
            caption = re.sub(r'#\d+', '', content).strip() if content else None
            await context.bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)
        elif update.message.video:
            # Nếu là video, gửi kèm chú thích (nếu có)
            video = update.message.video.file_id
            caption = re.sub(r'#\d+', '', content).strip() if content else None
            await context.bot.send_video(chat_id=channel_id, video=video, caption=caption)
        # Thêm xử lý cho các loại tin nhắn khác nếu cần



# Tạo một ứng dụng bot với token của bạn.
app = ApplicationBuilder().token(TOKEN_BOT).build()

# Thêm một MessageHandler để xử lý tất cả tin nhắn văn bản gửi đến bot
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO & ~filters.COMMAND, forward_to_channels))

# Bắt đầu bot
app.run_polling()