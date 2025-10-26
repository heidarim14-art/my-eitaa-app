import requests
import time
import json

# توکن رسمی ایتای خود را اینجا قرار دهید
BOT_TOKEN =bot88933:ad56971f-9559-47e0-a99b-06e3e74ac24a
API_URL = f"https://eitaa.com/bot{BOT_TOKEN}/"
last_update_id = 0

print("✅ ربات آماده دریافت فایل است. لطفاً فایل‌های خود را یک به یک برای ربات ارسال کنید...")
print("بعد از ارسال هر فایل، اطلاعات آن در اینجا نمایش داده می‌شود.")

while True:
    try:
        response = requests.get(API_URL + "getUpdates", params={'offset': last_update_id + 1, 'timeout': 60})
        updates = response.json()
        if updates.get("result"):
            for update in updates["result"]:
                last_update_id = update["update_id"]
                print("\n" + "="*50)
                print("🎉 فایل جدید دریافت شد! اطلاعات کامل:")
                # چاپ کامل آپدیت با فرمت زیبا
                print(json.dumps(update, indent=2, ensure_ascii=False))
                print("="*50 + "\n")
    except:
        pass
    time.sleep(1)