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
    user_message = update.message.text

    # Tìm kiếm kí hiệu đánh dấu và số theo sau trong tin nhắn
    matches = re.findall(r'#(\d+)', user_message)
    target_channels = []
    for match in matches:
        for digit in match:
            channel_id = CHANNELS.get(digit)
            if channel_id and channel_id not in target_channels:
                target_channels.append(channel_id)

    # Gửi tin nhắn đến các channel tương ứng
    for channel_id in target_channels:
        if update.message.text:
            # Loại bỏ kí hiệu đánh dấu khỏi tin nhắn trước khi gửi
            message_to_send = re.sub(r'#\d+', '', user_message).strip()
            await context.bot.send_message(chat_id=channel_id, text=message_to_send)
        elif update.message.photo:
            photo = update.message.photo[-1]
            await context.bot.send_photo(chat_id=channel_id, photo=photo.file_id, caption=update.message.caption)
        elif update.message.video:
            await context.bot.send_video(chat_id=channel_id, video=update.message.video.file_id, caption=update.message.caption)


# Tạo một ứng dụng bot với token của bạn.
app = ApplicationBuilder().token(TOKEN_BOT).build()

# Thêm một MessageHandler để xử lý tất cả tin nhắn văn bản gửi đến bot
app.add_handler(MessageHandler(filters.ALL &~filters.COMMAND, forward_to_channels))

# Bắt đầu bot
app.run_polling()