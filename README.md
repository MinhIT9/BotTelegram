requirements.txt: Danh sách các gói Python cần thiết để chạy ứng dụng. 
Sử dụng lệnh **pip install -r requirements.txt** để cài đặt tất cả cùng một lúc.
lấy gói "pip freeze > requirements.txt"
pyinstaller --onefile your_main_script.py
---------
1. Tạo và Sử dụng Môi trường Ảo
Tạo môi trường ảo: python -m venv env
Kích hoạt môi trường ảo:
- Windows: env\Scripts\activate
- MacOS và Linux: source env/bin/activate
2. Quản lý Phụ thuộc
Cài đặt các thư viện: pip install numpy pandas flask
Xuất danh sách phụ thuộc vào requirements.txt:
    - pip freeze > requirements.txt : Xuất ALL
    - pip install -r requirements.txt : Cài ALL
Tắt mt ảo: deactivate
3. Tạo Script tự động
- Tạo một Batch Script trên Windows (run.bat):
@echo off
call env\Scripts\activate
python app.py

- Tạo một Shell Script trên macOS/Linux (run.sh):
#!/bin/bash
source env/bin/activate
python app.py
---------
Tính năng Đang Có:
1. Gửi tin nhắn tới BOT - tự động chuyển tin nhắn đến các Channel do BOT quản lý
- Gửi được tin nhắn kèm 1 ảnh hoặc 1 video có caption = Giữ nguyên định dạng
- Có thể chỉnh sửa được tin nhắn đã gửi (Lưu ý sẽ bị mất FORMAT)
- ADD-EDIT-SHOW channels do BOT làm ADMIN


2. Tính Năng Trong Tương Lai:
- Gửi tin nhắn tới channel theo dạng ALBUMS
- Gửi tin nhắn có format kèm theo
- EDIT ảnh/video trong tin nhắn cũ
- REMOVE Channel
- Tính năng LOG các hành động, lỗi, tạo 1 Channel riêng để nhận các LOG này
- Phân quyền cho BOT, chỉ cho các tài khoản được add vào LIST ADMIN thì BOT mới chuyển tin nhắn qua CHANNEL bởi các ADMIN
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
---------
Phiên bản V2.1 - Thêm tính năng
- SetChanne: 
    Cú pháp: /setChannel <numberID> <ChannelID>: 
    Nếu đã tổn tại NumberID thì thay đôi ChannelID
    Nếu chưa tồn tại NumberID thì thêm mới 1 ChannelID khác
---------
Phiên Bản V2.1.1
- Cập nhật certifi SSL cho API ok
---------
Phiên bản V2.2
- Thêm tính năng cho lệnh setChannel, showChannel
    setChannel sẽ tự động lấy luôn tên channel và lưu vào API
    showChannel sẽ hiển thị thêm Tên Channel
---------
Phiên bản V2.3
- Rút gọn các hàm bên trong file API.py
---------
Version V2.4:
- Fix lỗi setChannel và gửi tin nhắn đến các Channel
- Tối ưu code
- Thay đổi qua sử dụng biến môi trường
---------
Version 2.5
- Fix lỗi: gửi tin nhắn có định dạng B U I Hyperlink
- Lấy dữ liệu CHANNELS lần đầu khi khởi động BOT
- Cải thiện tốt độ load tin nhắn và gửi tin nhắn đến channel
---------
Version 2.5.1 
- Thêm chức năng xoá tin nhắn /rm ở cuối tin nhắn edit
- Sử dụng tính năng copy_message cho tin nhắn gửi đến channel,ko dùng được trong edit
