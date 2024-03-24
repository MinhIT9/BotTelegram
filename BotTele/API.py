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
