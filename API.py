# API.py
import aiohttp
import json

# Lấy dữ liệu Channels từ API
async def fetch_channel_data(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                channel_data = await response.json()
                return channel_data, None
            else:
                return None, "Failed to fetch channel data."
            
# Lấy dữ liệu message_id_mapping từ API
async def fetch_message_id_mapping(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                # Giả sử chúng ta muốn trích xuất phần message_id_mapping từ phần tử đầu tiên của mảng
                # Kiểm tra nếu dữ liệu trả về là một mảng và có ít nhất một phần tử
                if data and isinstance(data, list) and 'message_id_mapping' in data[0]:
                    mapping = data[0]['message_id_mapping']
                    return mapping, None
                else:
                    return None, "Data format is incorrect or message_id_mapping not found"
            else:
                return None, "Failed to fetch message ID mapping"

# Update messageIdMapping
async def update_message_id_mapping_on_api(api_url, message_id_mapping_id, message_id_mapping_data):
    # Xây dựng URL bằng cách thêm ID vào API URL
    url_with_id = f"{api_url}/{message_id_mapping_id}"
    async with aiohttp.ClientSession() as session:
        # Chuyển dữ liệu message_id_mapping thành JSON
        data = json.dumps({"message_id_mapping": message_id_mapping_data})
        print("data to API: ", data)
        headers = {'Content-Type': 'application/json'}
        async with session.put(url_with_id, data=data, headers=headers) as response:
            
            # In ra mã trạng thái và nội dung phản hồi từ API
            print(f"Status Code: {response.status}")
            response_text = await response.text()  # Lấy nội dung phản hồi dưới dạng text
            print(f"Response from API: {response_text}")

            if response.status == 200:
                print("message_id_mapping successfully updated on API")
                # Đảm bảo việc sử dụng response.json() ở đây
                return await response.json()  # Giả định API trả về JSON
            else:
                print("Failed to update message_id_mapping on API")
                return None

#  xử lý việc cập nhật hoặc thêm mới channel - START
async def set_or_update_channel(api_url, channel_number, channel_id):
    channel_data, error = await fetch_channel_data(api_url)
    if error:
        print(f"Error fetching channels: {error}")
        return None, "Failed to fetch channels data."

    existing_channel = next((item for item in channel_data if item['channel_number'] == channel_number), None)
    
    # Nếu channel_number đã tồn tại, cập nhật channel_id
    if existing_channel:
        return await update_channel(api_url, existing_channel['id'], {'channel_number': channel_number, 'channel_id': channel_id})
    else:
        # Nếu không tồn tại, thêm mới
        return await add_new_channel(api_url, {'channel_number': channel_number, 'channel_id': channel_id})
    
async def update_channel(api_url, channel_id, channel_data):
    url_with_id = f"{api_url}/{channel_id}"
    async with aiohttp.ClientSession() as session:
        data = json.dumps(channel_data)
        headers = {'Content-Type': 'application/json'}
        async with session.put(url_with_id, data=data, headers=headers) as response:
            if response.status == 200:
                return await response.json(), None
            else:
                return None, "Failed to update channel."
            
async def add_new_channel(api_url, channel_data):
    async with aiohttp.ClientSession() as session:
        data = json.dumps(channel_data)
        headers = {'Content-Type': 'application/json'}
        async with session.post(api_url, data=data, headers=headers) as response:
            if response.status in [200, 201]:
                return await response.json(), None
            else:
                return None, "Failed to add new channel."
#  xử lý việc cập nhật hoặc thêm mới channel - END