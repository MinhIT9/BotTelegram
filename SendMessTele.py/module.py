from telegram import Update
from telegram.ext import ContextTypes
import re
from config import CHANNELS, message_id_mapping, fetch_channel_data, update_channels, api_url



# Fucntion này có chức năng đăng bài trên BOT lên các Channel khác
# Có chức năng chỉnh sửa
# Chưa có chức năng gửi ảnh video theo dạng albums
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update_channels()

    global message_id_mapping
    print("Channels: ", CHANNELS)
    
    # Xử lý tin nhắn mới
    if update.message:
        chat_id = update.message.chat_id
        original_message_id = update.message.message_id
        content = update.message.text or update.message.caption

        matches = re.findall(r'#(\d+)', content if content else '')
        target_channels = [CHANNELS.get(digit) for match in matches for digit in match if CHANNELS.get(digit)]

        for channel_id in target_channels:
            if update.message.text:
                message_to_send = re.sub(r'#\d+', '', content).strip()
                sent_message = await context.bot.send_message(chat_id=channel_id, text=message_to_send)
            elif update.message.photo:
                photo = update.message.photo[-1].file_id
                caption = re.sub(r'#\d+', '', content).strip() if content else None
                sent_message = await context.bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)
            elif update.message.video:
                video = update.message.video.file_id
                caption = re.sub(r'#\d+', '', content).strip() if content else None
                sent_message = await context.bot.send_video(chat_id=channel_id, video=video, caption=caption)
            else:
                continue

            if chat_id not in message_id_mapping:
                message_id_mapping[chat_id] = {}
            if original_message_id not in message_id_mapping[chat_id]:
                message_id_mapping[chat_id][original_message_id] = {}
            message_id_mapping[chat_id][original_message_id][channel_id] = sent_message.message_id
        pass
        print("message_id_mapping: ", message_id_mapping)
    # Xử lý tin nhắn chỉnh sửa
    elif update.edited_message:
        chat_id = update.edited_message.chat_id
        original_message_id = update.edited_message.message_id

        if chat_id in message_id_mapping and original_message_id in message_id_mapping[chat_id]:
            # Dựa vào nội dung mới để xác định loại cập nhật
            new_text = update.edited_message.text
            new_caption = update.edited_message.caption

            for channel_id, forwarded_message_id in message_id_mapping[chat_id][original_message_id].items():
                # Nếu tin nhắn chỉnh sửa có văn bản, cập nhật văn bản của tin nhắn
                if new_text:
                    await context.bot.edit_message_text(chat_id=channel_id, message_id=forwarded_message_id, text=new_text)
                # Nếu tin nhắn chỉnh sửa có caption, và đây là hình ảnh hoặc video, cập nhật caption
                elif new_caption:
                    await context.bot.edit_message_caption(chat_id=channel_id, message_id=forwarded_message_id, caption=new_caption)

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

async def show_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Đảm bảo rằng CHANNELS đã được cập nhật.
    # Chỉ cần gọi update_channels nếu CHANNELS là rỗng hoặc bạn muốn cập nhật lại nó.
    await update_channels()

    # Sau khi đảm bảo CHANNELS đã được cập nhật, hiển thị nó.
    if CHANNELS:
        message_text = "Current Channels:\n"
        for number, channel_id in CHANNELS.items():
            message_text += f"Number {number}: {channel_id}\n"
        await update.message.reply_text(message_text)
    else:
        await update.message.reply_text("No channels to display or failed to update channels.")

