# API.py
import aiohttp
import json
import ssl
import certifi

# Hàm Chứng Chỉ SSL Mặc Định
async def get_client_session() -> aiohttp.ClientSession:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    return aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context))

# Sử dụng một ClientSession duy nhất cho tất cả các yêu cầu
session = None

# Lấy dữ liệu Channels từ API
async def fetch_channel_data(api_url):
    global session
    if session is None:
        session = await get_client_session()
        
    try:
        async with session.get(api_url) as response:
            if response.status == 200:
                return await response.json(), None
            else:
                return None, f"Failed to fetch channel data. Status: {response.status}"
    except aiohttp.ClientError as e:
        return None, f"An error occurred: {str(e)}"
            
# Lấy dữ liệu message_id_mapping từ API
async def fetch_message_id_mapping(api_url):
    global session
    if session is None:
        session = await get_client_session()
        
    try:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                if data and isinstance(data, list) and 'message_id_mapping' in data[0]:
                    return data[0]['message_id_mapping'], None
                else:
                    return None, "Data format is incorrect or message_id_mapping not found"
            else:
                return None, f"Failed to fetch message ID mapping. Status: {response.status}"
    except aiohttp.ClientError as e:
        return None, f"An error occurred: {str(e)}"

# Update messageIdMapping
async def update_message_id_mapping_on_api(api_url, message_id_mapping_id, message_id_mapping_data):
    global session
    if session is None:
        session = await get_client_session()
    
    try:
        url_with_id = f"{api_url}/{message_id_mapping_id}"
        data = json.dumps({"message_id_mapping": message_id_mapping_data})
        headers = {'Content-Type': 'application/json'}
        async with session.put(url_with_id, data=data, headers=headers) as response:
            if response.status == 200:
                return await response.json(), None
            else:
                return None, f"Failed to update message_id_mapping on API. Status: {response.status}"
    except aiohttp.ClientError as e:
        return None, f"An error occurred: {str(e)}"

#  xử lý việc cập nhật hoặc thêm mới channel - START
async def set_or_update_channel(api_url, channel_number, channel_id, channel_name):
    global session
    if session is None:
        session = await get_client_session()
    
    try:
        channel_data, error = await fetch_channel_data(api_url)
        if error:
            return None, error
        
        existing_channel = next((item for item in channel_data if item['channel_number'] == channel_number), None)
        
        if existing_channel:
            return await update_channel(api_url, existing_channel['id'], {'channel_number': channel_number, 'channel_id': channel_id, 'channel_name': channel_name})
        else:
            return await add_new_channel(api_url, {'channel_number': channel_number, 'channel_id': channel_id, 'channel_name': channel_name})
    except aiohttp.ClientError as e:
        return None, f"An error occurred: {str(e)}"
    
async def update_channel(api_url, channel_id, channel_data):
    global session
    if session is None:
        session = await get_client_session()
    
    try:
        url_with_id = f"{api_url}/{channel_id}"
        data = json.dumps(channel_data)
        headers = {'Content-Type': 'application/json'}
        async with session.put(url_with_id, data=data, headers=headers) as response:
            if response.status == 200:
                return await response.json(), None
            else:
                return None, f"Failed to update channel. Status: {response.status}"
    except aiohttp.ClientError as e:
        return None, f"An error occurred: {str(e)}"
            
async def add_new_channel(api_url, channel_data):
    global session
    if session is None:
        session = await get_client_session()
    
    try:
        data = json.dumps(channel_data)
        headers = {'Content-Type': 'application/json'}
        async with session.post(api_url, data=data, headers=headers) as response:
            if response.status in [200, 201]:
                return await response.json(), None
            else:
                return None, f"Failed to add new channel. Status: {response.status}"
    except aiohttp.ClientError as e:
        return None, f"An error occurred: {str(e)}"
#  xử lý việc cập nhật hoặc thêm mới channel - END

# Đừng quên đóng session khi không cần thiết nữa
async def close_session():
    global session
    if session:
        await session.close()
        session = None