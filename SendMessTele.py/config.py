import requests
from aiohttp  import ClientSession
import asyncio

TOKEN_BOT = '6500285460:AAEm_dyWXxszfm0T3DJmMFrRV4Ez6M8jQcg'
api_url = "https://6576fb06197926adf62cee4c.mockapi.io/api/channels"
CHANNELS = {}  # Khai báo CHANNELS ở đây

#Get Channels
async def fetch_channel_data(api_url):
    try:
        async with ClientSession() as session:
            async with session.get(api_url) as response:
                # print(f"Response Status: {response.status}")  # In trạng thái phản hồi
                if response.status == 200:
                    channel_data = await response.json()
                    # print(f"Channel Data: {channel_data}")  # In dữ liệu kênh
                    return channel_data, None
                else:
                    return None, "Failed to fetch channel data from API."
    except Exception as e:
        print(f"Error: {e}")  # In lỗi
        return None, str(e)
    
async def update_channels():
    global CHANNELS  # Sử dụng biến toàn cục CHANNELS
    channel_data, error = await fetch_channel_data(api_url)
    if channel_data:
        CHANNELS.clear()
        for channel in channel_data:
            number = channel.get('channel_number')
            channel_id = channel.get('channel_id')
            if number and channel_id:
                CHANNELS[number] = channel_id
    elif error:
        print("Error updating channels:", error)
        
# Gọi update_channels và sau đó in CHANNELS
async def main():
    await update_channels()
    # print(f"Updated CHANNELS: {CHANNELS}")  # In CHANNELS sau khi cập nhật
    # print(CHANNELS)  # In giá trị của CHANNELS sau khi cập nhật

# Sử dụng asyncio.run() để chạy hàm main
if __name__ == "__main__":
    asyncio.run(main())
    
# { chat_id: { original_message_id: forwarded_message_id }} 
message_id_mapping = {} 

# Danh sách các lệnh và mô tả của chúng
commands_list = [
    
    # ("/Start", "Khởi động bot và hiển thị thông điệp chào mừng."),
    ("/admin", "Hiển thị danh sách các lệnh hiện có của bot."),
    ("/setChannel", "Thiết lập hoặc thay đổi ID kênh. Cú pháp: /setchannel <number> <channel_id>"),
    ("/showChannel", "Hiển thị danh sách các kênh hiện tại."),
   
]
