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
    await update_messageIdMapping()

    # Xử lý tin nhắn gửi đi
    if update.message:
        chat_id = update.message.chat_id
        original_message_id = update.message.message_id
        content = update.message.text or update.message.caption

        matches = re.findall(r'#(\d+)', content if content else '')
        target_channels = [CHANNELS.get(digit) for match in matches for digit in match if CHANNELS.get(digit)]

        send_tasks = [send_message_to_channel(context, chat_id, channel_info, content, update, original_message_id) for channel_info in target_channels]
        await asyncio.gather(*send_tasks)

        await update_message_id_mapping_on_api(MESSAGE_ID_MAPPING_API, MESSAGE_ID_MAPPING_API_ID, message_id_mapping)

    elif update.edited_message:
        chat_id = update.edited_message.chat_id
        original_message_id = update.edited_message.message_id
        new_text = update.edited_message.text
        new_caption = update.edited_message.caption

        if chat_id in message_id_mapping and original_message_id in message_id_mapping[chat_id]:
            edit_tasks = [edit_message_in_channel(context, channel_id, forwarded_message_id, new_text, new_caption, original_message_id)
                          for channel_id, forwarded_message_id in message_id_mapping[chat_id][original_message_id].items()]
            await asyncio.gather(*edit_tasks)

async def send_message_to_channel(context, chat_id, channel_info, content, update, original_message_id):
    channel_id = channel_info['id']
    try:
        sent_message = None
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

        if sent_message:
            message_id_mapping.setdefault(chat_id, {}).setdefault(original_message_id, {})[channel_id] = sent_message.message_id
    except TelegramError as e:
        print(f"Error sending message to channel {channel_id}: {str(e)}")

async def edit_message_in_channel(context, channel_id, forwarded_message_id, new_text, new_caption, original_message_id):
    try:
        if new_text:
            await context.bot.edit_message_text(chat_id=channel_id, message_id=forwarded_message_id, text=clean_content(new_text))
        elif new_caption:
            await context.bot.edit_message_caption(chat_id=channel_id, message_id=forwarded_message_id, caption=clean_content(new_caption))
    except TelegramError as e:
        print(f"Error editing message in channel {channel_id}: {str(e)}")
