
import aiohttp

async def fetch_channel_data(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                channel_data = await response.json()
                return channel_data, None
            else:
                return None, "Failed to fetch channel data."

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
