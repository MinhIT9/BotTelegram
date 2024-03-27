from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, Application
from handlers_command import set_channel, show_channels, admin, start
from handlers_message import handle_message
from bot_config import TOKEN_BOT, update_channels
import asyncio

async def startup():
    print("Đang khởi động bot và cập nhật CHANNELS...")
    await update_channels()  # Gọi hàm cập nhật CHANNELS
    print("Khởi động thành công!")

def register_handlers(application: Application):
    # Show all Command
    application.add_handler(CommandHandler('admin', admin))
    application.add_handler(CommandHandler('start', start))

    # Forward and Edit Message
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    # Set Channels
    application.add_handler(CommandHandler("setChannel", set_channel))
    # Show Channel
    application.add_handler(CommandHandler('showChannel', show_channels))

def main():
    # Khởi tạo loop bất đồng bộ
    loop = asyncio.get_event_loop()

    # Chạy hàm startup bất đồng bộ
    loop.run_until_complete(startup())

    # Khởi tạo bot
    application = Application.builder().token(TOKEN_BOT).build()

    # Đăng ký các handlers
    register_handlers(application)
    
    # Chạy bot
    application.run_polling()

if __name__ == '__main__':
    main()
