import re
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from bot_config import CHANNELS, MESSAGE_ID_MAPPING_API, message_id_mapping, update_messageIdMapping, MESSAGE_ID_MAPPING_API_ID
from API import update_message_id_mapping_on_api

def clean_content(content):
    # Loại bỏ hashtags và khoảng trắng không cần thiết từ nội dung tin nhắn
    return re.sub(r'#\d+', '', content).strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Xử lý tin nhắn mới và tin nhắn đã chỉnh sửa

    if update.message:
        # Nếu là tin nhắn mới, gửi tin nhắn đến các kênh đích
        chat_id = update.message.chat_id
        original_message_id = update.message.message_id
        content = update.message.text or update.message.caption

        # Tìm kiếm các hashtag trong nội dung và xác định kênh đích
        matches = re.findall(r'#(\d+)', content if content else '')
        target_channels = [CHANNELS.get(digit) for match in matches for digit in match if CHANNELS.get(digit)]

        # Tạo và thực thi các tác vụ gửi tin nhắn đến kênh
        send_tasks = [send_message_to_channel(context, chat_id, channel_info, content, update, original_message_id) for channel_info in target_channels]
        await asyncio.gather(*send_tasks)

        # Cập nhật bản đồ ID tin nhắn sau khi gửi
        await update_message_id_mapping_on_api(MESSAGE_ID_MAPPING_API, MESSAGE_ID_MAPPING_API_ID, message_id_mapping)
        print("update_message_id_mapping_on_api SCUSSES!")

    elif update.edited_message:
        # Nếu tin nhắn được chỉnh sửa, cập nhật tin nhắn tương ứng trong các kênh
        chat_id = update.edited_message.chat_id
        original_message_id = update.edited_message.message_id
        new_text = update.edited_message.text
        new_caption = update.edited_message.caption

        # Kiểm tra và thực thi tác vụ chỉnh sửa tin nhắn trên các kênh
        if chat_id in message_id_mapping and original_message_id in message_id_mapping[chat_id]:
            edit_tasks = [edit_message_in_channel(context, channel_id, forwarded_message_id, new_text, new_caption, original_message_id)
                          for channel_id, forwarded_message_id in message_id_mapping[chat_id][original_message_id].items()]
            await asyncio.gather(*edit_tasks)

async def send_message_to_channel(context, chat_id, channel_info, content, update, original_message_id):
    # Gửi tin nhắn đến kênh đích và cập nhật bản đồ ID tin nhắn
    channel_id = channel_info['id']
    try:
        sent_message = None
        # Gửi tin nhắn dựa trên loại nội dung: văn bản, ảnh hoặc video
        if update.message.text:
            message_to_send = clean_content(content)
            sent_message = await context.bot.send_message(chat_id=channel_id, text=message_to_send, parse_mode='Markdown')
        elif update.message.photo:
            photo = update.message.photo[-1].file_id
            caption = clean_content(content) if content else None
            sent_message = await context.bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)
        elif update.message.video:
            video = update.message.video.file_id
            caption = clean_content(content) if content else None
            sent_message = await context.bot.send_video(chat_id=channel_id, video=video, caption=caption)
    
        # Cập nhật bản đồ ID tin nhắn sau khi gửi thành công
        if sent_message:
            message_id_mapping.setdefault(chat_id, {}).setdefault(original_message_id, {})[channel_id] = sent_message.message_id
    except TelegramError as e:
        # Xử lý lỗi khi gửi tin nhắn
        print(f"Error sending message to channel {channel_id}: {str(e)}")

async def edit_message_in_channel(context, channel_id, forwarded_message_id, new_text, new_caption, original_message_id):
    try:
        # Kiểm tra và chỉnh sửa văn bản hoặc chú thích của tin nhắn
        if new_text:
            # Nếu có văn bản mới, chỉnh sửa văn bản tin nhắn
            await context.bot.edit_message_text(chat_id=channel_id, message_id=forwarded_message_id, text=clean_content(new_text))
        elif new_caption:
            # Nếu có chú thích mới, chỉnh sửa chú thích của tin nhắn
            await context.bot.edit_message_caption(chat_id=channel_id, message_id=forwarded_message_id, caption=clean_content(new_caption))
    except TelegramError as e:
        # Xử lý lỗi khi chỉnh sửa tin nhắn
        print(f"Error editing message in channel {channel_id}: {str(e)}")
