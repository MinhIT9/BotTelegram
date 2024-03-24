# bot_config.py
from API import fetch_channel_data, fetch_message_id_mapping
import asyncio

CHANNELS = {}
message_id_mapping = {}


commands_list = [
    
    # ("/Start", "Khởi động bot và hiển thị thông điệp chào mừng."),
    ("/admin", "Hiển thị danh sách các lệnh hiện có của bot."),
    ("/setChannel", "Thiết lập hoặc thay đổi ID kênh. Cú pháp: /setchannel <number> <channel_id>"),
    ("/showChannel", "Hiển thị danh sách các kênh hiện tại."),
   
]


TOKEN_BOT = '6500285460:AAEm_dyWXxszfm0T3DJmMFrRV4Ez6M8jQcg'
CHANNEL_API = "https://6576fb06197926adf62cee4c.mockapi.io/api/channels"
MESSAGE_ID_MAPPING_API = "https://6576fb06197926adf62cee4c.mockapi.io/api/messageIdMapping"



# Cập nhật CHANNELS
async def update_channels():
    global CHANNELS
    channel_data, error = await fetch_channel_data(CHANNEL_API)
    if channel_data:
        CHANNELS.clear()
        for channel in channel_data:
            number = channel.get('channel_number')
            channel_id = channel.get('channel_id')
            if number and channel_id:
                CHANNELS[number] = channel_id



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
    data_messIdMapping, error = await fetch_message_id_mapping(MESSAGE_ID_MAPPING_API)
    if error:
        print(f"Error: {error}")
    else:
        # message_id_mapping.clear()
        # Sử dụng hàm chuyển đổi ở đây
        converted_data = convert_keys_to_int(data_messIdMapping)
        message_id_mapping.update(converted_data)
        print("Fetched message_id_mapping successfully.")
        # print(message_id_mapping)



# async def main():
#     await update_messageIdMapping()
    
    
# if __name__ == '__main__':
#     asyncio.run(main())
# print(message_id_mapping)