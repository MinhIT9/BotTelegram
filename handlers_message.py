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
        
         # Nếu tin nhắn được chỉnh sửa
        edited_text = update.edited_message.text or update.edited_message.caption
        if edited_text.endswith('/rm'):
            # Xác định và xoá tin nhắn gốc nếu nó được chỉnh sửa để thêm "/del" vào cuối
            await delete_message_in_channels(update.edited_message.chat_id, update.edited_message.message_id, context)
            # Xoá tin nhắn gốc trên Telegram
            await context.bot.delete_message(chat_id=update.edited_message.chat_id, message_id=update.edited_message.message_id)

        # Kiểm tra và thực thi tác vụ chỉnh sửa tin nhắn trên các kênh
        if chat_id in message_id_mapping and original_message_id in message_id_mapping[chat_id]:
            edit_tasks = [edit_message_in_channel(context, channel_id, forwarded_message_id, new_text, new_caption, original_message_id)
                          for channel_id, forwarded_message_id in message_id_mapping[chat_id][original_message_id].items()]
            await asyncio.gather(*edit_tasks)

async def send_message_to_channel(context, chat_id, channel_info, content, update, original_message_id):
    channel_id = channel_info['id']
    try:
        # Copy tin nhắn đến kênh đích dựa trên loại nội dung
        if update.message.text or update.message.photo or update.message.video:
            sent_message = await context.bot.copy_message(
                chat_id=channel_id,
                from_chat_id=chat_id,
                message_id=original_message_id
            )
            
            # Cập nhật bản đồ ID tin nhắn sau khi gửi thành công
            message_id_mapping.setdefault(chat_id, {}).setdefault(original_message_id, {})[channel_id] = sent_message.message_id
    except TelegramError as e:
        print(f"Error sending/copying message to channel {channel_id}: {str(e)}")

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



async def delete_message_in_channels(chat_id, message_id, context):
    if chat_id in message_id_mapping and message_id in message_id_mapping[chat_id]:
        for channel_id, forwarded_message_id in message_id_mapping[chat_id][message_id].items():
            try:
                await context.bot.delete_message(chat_id=channel_id, message_id=forwarded_message_id)
                print(f"Deleted message {forwarded_message_id} in channel {channel_id}")
            except TelegramError as e:
                print(f"Error deleting message in channel {channel_id}: {str(e)}")
        # Xoá mapping sau khi xoá tin nhắn
        del message_id_mapping[chat_id][message_id]
        # Đừng quên cập nhật message_id_mapping trên server/api nếu cần
        await update_message_id_mapping_on_api(MESSAGE_ID_MAPPING_API, MESSAGE_ID_MAPPING_API_ID, message_id_mapping)
