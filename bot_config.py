# bot_config.py
import asyncio, json, os
from dotenv  import load_dotenv
from API import fetch_channel_data, fetch_message_id_mapping, update_message_id_mapping_on_api
from telegram import Bot

load_dotenv("env.env")

# Lấy giá trị biến môi trường
TOKEN_BOT = os.getenv('TOKEN_BOT')  # Lấy từ biến môi trường
CHANNEL_API = os.getenv('CHANNEL_API')  # Lấy từ biến môi trường
MESSAGE_ID_MAPPING_API = os.getenv('MESSAGE_ID_MAPPING_API')  # Lấy từ biến môi trường
MESSAGE_ID_MAPPING_API_ID = os.getenv('MESSAGE_ID_MAPPING_API_ID')  # Sử dụng ID phù hợp với môi trường của bạn

bot = Bot(token=TOKEN_BOT)
CHANNELS = {}
message_id_mapping = {}

#ADMIN
commands_list = [
    ("/admin", "Hiển thị danh sách các lệnh hiện có của bot."),
    ("/setChannel", "Thiết lập hoặc thay đổi ID kênh."),
    ("/showChannel", "Hiển thị danh sách các kênh hiện tại.")
]

# Cập nhật CHANNELS
async def update_channels():
    global CHANNELS
    channel_data, error = await fetch_channel_data(CHANNEL_API)
    if channel_data:
        CHANNELS.clear()
        for channel in channel_data:
            number = channel.get('channel_number')
            channel_id = channel.get('channel_id')
            channel_name = channel.get('channel_name')  # Lấy channel_name từ dữ liệu
            if number and channel_id and channel_name:
                CHANNELS[number] = {'id': channel_id, 'name': channel_name}


# Hàm Chuyển Đổi từ chuỗi sang số nguyên
def convert_keys_to_int(mapping):
    converted_mapping = {}
    for key, value in mapping.items():
        # Chuyển đổi khóa từ chuỗi sang số nguyên, nếu có thể
        int_key = int(key) if key.isdigit() else key
        if isinstance(value, dict):
            # Đệ quy nếu giá trị là một dictionary
            converted_mapping[int_key] = convert_keys_to_int(value)
        else:
            # Nếu không, giữ nguyên giá trị
            converted_mapping[int_key] = value
    return converted_mapping

# Cập nhật message_id_mapping
async def update_messageIdMapping():
    # Sử dụng MESSAGE_ID_MAPPING_API_ID khi gọi hàm fetch_message_id_mapping
    data_messIdMapping, error = await fetch_message_id_mapping(MESSAGE_ID_MAPPING_API, MESSAGE_ID_MAPPING_API_ID)
    if error:
        print(f"Error: {error}")
    else:
        # Không cần lọc, vì data_messIdMapping đã trực tiếp là dữ liệu bạn muốn
        message_id_mapping_data = data_messIdMapping.get("message_id_mapping", {})
        # Sử dụng hàm chuyển đổi ở đây
        converted_data = convert_keys_to_int(message_id_mapping_data)
        message_id_mapping.update(converted_data)
        print("Fetched and updated message_id_mapping successfully with id:", MESSAGE_ID_MAPPING_API_ID)

