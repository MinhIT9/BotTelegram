# API.py
import aiohttp
import json
import ssl
import certifi

# Hàm trợ giúp để tạo và thực hiện yêu cầu HTTP
async def make_request(method, url, data=None, headers=None):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
        try:
            request_func = getattr(session, method)
            async with request_func(url, json=data, headers=headers) as response:
                if response.status in [200, 201]:
                    return await response.json(), None
                else:
                    return None, f"Failed to {method} request. Status: {response.status}"
        except aiohttp.ClientError as e:
            return None, f"An error occurred: {str(e)}"

# Lấy dữ liệu Channels từ API
async def fetch_channel_data(api_url):
    return await make_request("get", api_url)
            
# Lấy dữ liệu message_id_mapping từ API
async def fetch_message_id_mapping(api_url):
    result, error = await make_request("get", api_url)
    if result and isinstance(result, list) and 'message_id_mapping' in result[0]:
        return result[0]['message_id_mapping'], None
    else:
        return None, "Data format is incorrect or message_id_mapping not found" if not error else error

# Update messageIdMapping
async def update_message_id_mapping_on_api(api_url, message_id_mapping_id, message_id_mapping_data):
    url_with_id = f"{api_url}/{message_id_mapping_id}"
    data = {"message_id_mapping": message_id_mapping_data}
    headers = {'Content-Type': 'application/json'}
    return await make_request("put", url_with_id, data=data, headers=headers)

#  xử lý việc cập nhật hoặc thêm mới channel - START
async def set_or_update_channel(api_url, channel_number, channel_id, channel_name):
    channel_data, error = await fetch_channel_data(api_url)
    if error:
        return None, error

    existing_channel = next((item for item in channel_data if item['channel_number'] == channel_number), None)

    if existing_channel:
        return await update_channel(api_url, existing_channel['id'], {'channel_number': channel_number, 'channel_id': channel_id, 'channel_name': channel_name})
    else:
        return await add_new_channel(api_url, {'channel_number': channel_number, 'channel_id': channel_id, 'channel_name': channel_name})

async def update_channel(api_url, channel_id, channel_data):
    url_with_id = f"{api_url}/{channel_id}"
    return await make_request("put", url_with_id, data=channel_data, headers={'Content-Type': 'application/json'})

async def add_new_channel(api_url, channel_data):
    return await make_request("post", api_url, data=channel_data, headers={'Content-Type': 'application/json'})

#  xử lý việc cập nhật hoặc thêm mới channel - END
