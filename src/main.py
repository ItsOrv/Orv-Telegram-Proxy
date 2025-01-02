import asyncio
import threading
from bot import client, bot, schedule_cleaning
from app import app, refresh_proxies

# تابع برای اجرای سرور Flask
def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)  # غیرفعال کردن reloader و debug

# تابع برای اجرای ربات تلگرام (Telethon)
async def run_telegram():
    # شروع به کار ربات
    await client.start()

    # اجرای وظایف زمان‌بندی‌شده
    asyncio.create_task(schedule_cleaning())

    # اجرای ربات تلگرام تا زمانی که قطع شود
    await client.run_until_disconnected()

# تابع اصلی برای اجرای هر دو سرور
def main():
    # اجرای سرور Flask در یک نخ جداگانه
    threading.Thread(target=run_flask, daemon=True).start()

    # اجرای ربات تلگرام در حالت async
    asyncio.run(run_telegram())

if __name__ == "__main__":
    # شروع به کار برنامه
    main()
