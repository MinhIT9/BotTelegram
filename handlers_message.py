import re
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from bot_config import CHANNELS, MESSAGE_ID_MAPPING_API, message_id_mapping, update_channels, update_messageIdMapping, MESSAGE_ID_MAPPING_API_ID
from API import update_message_id_mapping_on_api

def clean_content(content):
    # Làm sạch nội dung tin nhắn bằng cách loại bỏ các hashtag và khoảng trắng thừa
    return re.sub(r'#\d+', '', content).strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Cập nhật dữ liệu các kênh và message ID mapping từ API
    await update_channels()
    await update_messageIdMapping()
    
    # print("CHANNELS: ", CHANNELS)
    # print("MessageIDmapping: ", message_id_mapping)

    # Xử lý tin nhắn gửi đi
    if update.message:
        chat_id = update.message.chat_id
        original_message_id = update.message.message_id
        content = update.message.text or update.message.caption

        # Tìm các kênh mục tiêu dựa trên hashtag trong nội dung tin nhắn
        matches = re.findall(r'#(\d+)', content if content else '')

        target_channels = []
        for match in matches:
            for digit in match:
                if channel_info := CHANNELS.get(digit):
                    target_channels.append(channel_info)
        
        for channel_info in target_channels:
            channel_id = channel_info['id']
            print("Sending message to Channel ID: ", channel_id)

            try:
                # Sử dụng copy_message để sao chép tin nhắn gốc sang channel mục tiêu
                sent_message = await context.bot.copy_message(
                    chat_id=channel_id,
                    from_chat_id=chat_id,
                    message_id=original_message_id
                )
                print("sent_message: ", sent_message)

                # Cập nhật mapping cho tin nhắn được gửi thành công
                if sent_message:
                    message_id_mapping.setdefault(chat_id, {}).setdefault(original_message_id, {})[channel_id] = sent_message.message_id

            except TelegramError as e:
                print(f"Error sending message to channel {channel_id}: {str(e)}")

        # Cập nhật mapping API sau khi gửi tin nhắn
        await update_message_id_mapping_on_api(MESSAGE_ID_MAPPING_API, MESSAGE_ID_MAPPING_API_ID, message_id_mapping)

    elif update.edited_message:
        # Xử lý tin nhắn được chỉnh sửa
        chat_id = update.edited_message.chat_id
        original_message_id = update.edited_message.message_id

        if chat_id in message_id_mapping and original_message_id in message_id_mapping[chat_id]:
            new_text = update.edited_message.text
            new_caption = update.edited_message.caption

            for channel_id, forwarded_message_id in message_id_mapping[chat_id][original_message_id].items():
                try:
                    if new_text:
                        await context.bot.edit_message_text(chat_id=channel_id, message_id=forwarded_message_id, text=clean_content(new_text))
                    elif new_caption:
                        await context.bot.edit_message_caption(chat_id=channel_id, message_id=forwarded_message_id, caption=clean_content(new_caption))
                except TelegramError as e:
                    print(f"Error editing message in channel {channel_id}: {str(e)}")
