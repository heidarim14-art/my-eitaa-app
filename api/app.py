from flask import Flask, request, jsonify
import requests
import os

# این خط برای ورسل مهم است تا بداند فایل‌های استاتیک کجا هستند
app = Flask(__name__, static_folder='../static', static_url_path='')

# --- تنظیمات ربات ---
# توکن و شناسه‌ها را از متغیرهای محیطی ورسل می‌خوانیم
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LEAD_MAGNET_PDF_ID = os.environ.get("LEAD_MAGNET_PDF_ID")
LEAD_MAGNET_AUDIO_ID = os.environ.get("LEAD_MAGNET_AUDIO_ID") # شناسه فایل صوتی
EITAA_API_URL = f"https://eitaa.com/bot{BOT_TOKEN}/"

# --- توابع کمکی برای ارسال به ایتا ---

def send_message(chat_id, text):
    url = EITAA_API_URL + "sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

def send_document(chat_id, file_id, caption=""):
    url = EITAA_API_URL + "sendDocument"
    payload = {'chat_id': chat_id, 'document': file_id, 'caption': caption}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Error sending document: {e}")

# تابع جدید برای ارسال فایل صوتی
def send_audio(chat_id, file_id, caption=""):
    url = EITAA_API_URL + "sendAudio"
    payload = {'chat_id': chat_id, 'audio': file_id, 'caption': caption}
    try:
        requests.post(url, json=payload, timeout=10)
        return True
    except Exception as e:
        print(f"Error sending audio: {e}")
        return False

# --- مسیر اصلی که "چهره برنامه" را نمایش می‌دهد ---
@app.route('/')
def index():
    return app.send_static_file('index.html')

# --- مسیری که اطلاعات کاربر را دریافت می‌کند ---
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json
    chat_id = data.get('chat_id')
    phone = data.get('phone')

    if not chat_id or not phone:
        return jsonify({"status": "error", "message": "Missing data."}), 400

    print(f"✅ Vercel Lead! | ChatID: {chat_id}, Phone: {phone}")

    # --- سناریوی ارسال چندمرحله‌ای ---
    # ۱. ارسال پیام متنی اولیه
    send_message(chat_id, "دمت گرم! اینم از جزوه ۱۰۰ جمله کاربردی که قولش رو داده بودم 👇")

    # ۲. ارسال فایل PDF
    send_document(chat_id, LEAD_MAGNET_PDF_ID)

    # ۳. ارسال فایل صوتی
    success = send_audio(chat_id, LEAD_MAGNET_AUDIO_ID, "اینم از فایل صوتی توضیحات تکمیلی من. حتماً گوش کن تا تلفظ‌ها رو کامل یاد بگیری! 🎧")
    
    if success:
        return jsonify({"status": "ok", "message": "All files sent."})
    else:
        return jsonify({"status": "error", "message": "Failed to send audio file."})

# این متغیر app باید در سطح ماژول باشد تا ورسل آن را پیدا کند
# نیازی به if __name__ == '__main__': در ورسل نیست