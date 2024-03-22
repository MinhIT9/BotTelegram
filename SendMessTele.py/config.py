TOKEN_BOT = '6500285460:AAEm_dyWXxszfm0T3DJmMFrRV4Ez6M8jQcg'
CHANNELS = {
    '1': '@Chan223a',
    '2': '@chanws1',
    '3': '@chan9090s',
    '4': '-1002133340256'
}

message_id_mapping = {}  # { chat_id: { original_message_id: forwarded_message_id }} 

# Danh sách các lệnh và mô tả của chúng
commands_list = [
    
    # ("/Start", "Khởi động bot và hiển thị thông điệp chào mừng."),
    ("/admin", "Hiển thị danh sách các lệnh hiện có của bot."),
    ("/setChannel", "Thiết lập hoặc thay đổi ID kênh. Cú pháp: /setchannel <number> <channel_id>"),
    ("/showChannel", "Hiển thị danh sách các kênh hiện tại."),
   
]
