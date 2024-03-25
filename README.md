requirements.txt: Danh sách các gói Python cần thiết để chạy ứng dụng. 
Sử dụng lệnh **pip install -r requirements.txt** để cài đặt tất cả cùng một lúc.
lấy gói "pip freeze"
---------
Phiên bản V2.0
1. Chức năng hoàn thành
- Gửi tin nhắn tới BOT, BOT tự động chuyển tin nhắn đến các Channel chỉ định qua dấu # ví dụ (#123)
    - Chỉ gửi được TEXT, PHOTO, VIDEO, caption kèm ảnh
- Chỉnh sửa tin nhắn được gửi tới BOT
    - Chỉnh sửa được TEXT
    - Chỉ EDIT được CAPTION của PHOTO và VIDEO
- Lấy danh sách channel từ API và hiển thị khi sử dụng lệnh /showChannel
- Cập nhật message_id_mapping khi SEND, EDIT tin nhắn tới BOT 
2. Chức năng cần thêm
- Gửi tin nhắn tới channel theo dạng ALBUMS
- EDIT ảnh đã gửi trước đó
- ADD, EDIT, REMOVE Channel
- Tính năng LOG các hành động, lỗi, tạo 1 Channel riêng để nhận các LOG này
---------
Phiên bản V2.1
1. Thêm tính năng
- SetChanne: 
    Cú pháp: /setChannel <numberID> <ChannelID>: 
    Nếu đã tổn tại NumberID thì thay đôi ChannelID
    Nếu chưa tồn tại NumberID thì thêm mới 1 ChannelID khác
    
2. Tính năng cần thêm
- Gửi tin nhắn tới channel theo dạng ALBUMS
- EDIT ảnh đã gửi trước đó
- REMOVE Channel
- Tính năng LOG các hành động, lỗi, tạo 1 Channel riêng để nhận các LOG này
---------
Phiên Bản V2.1.1
- Cập nhật certifi SSL cho API 
---------
Phiên bản V2.2
- Thêm tính năng cho lệnh setChannel, showChannel
    setChannel sẽ tự động lấy luôn tên channel và lưu vào API
    showChannel sẽ hiển thị thêm Tên Channel
