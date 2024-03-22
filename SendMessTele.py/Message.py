from telegram import Update
from telegram.ext import ContextTypes
import re
from config import *

# Fucntion này có chức năng đăng bài trên BOT lên các Channel khác
# Có chức năng chỉnh sửa
# Chưa có chức năng gửi ảnh video theo dạng albums

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global message_id_mapping
    
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
    if update.message:
        # Logic gửi tin nhắn mới như đã thảo luận trước đó.
        pass

    # Xử lý tin nhắn chỉnh sửa
    if update.edited_message:
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