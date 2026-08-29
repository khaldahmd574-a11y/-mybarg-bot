import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import os
from telethon import TelegramClient, events
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

API_ID = 39120728
API_HASH = '1deec8393ca5aa05c54c0c7e280377d4'
BOT_TOKEN = '8782796916:AAGKs4vGK6s302vNpRAJ_3lU0YwJOHR8ybA'

SUBSCRIBERS_USERNAMES = [
    "abood1317",
    "shaybq",
    "Waaaaaaa33"
]

KEYWORDS = [
    "جازان", "صبيا", "خضيره", "رديس", "القُمري",
    "الدرب", "صامطه", "مرحوه", "المضايا", "الحقل", "بيت الرومسي",
    "البدء", "المشحراه", "المضايا", "الراشد", "ماك", "كادي", "المجمع",
    "مخطط", "احتاج", "ابغى", "تفضل", "مين",
    "يوصل", "تروح", "ابتسام",
    "اراجع", "راجع", "نبغى", "السوق", "دومات", "باازم",
    "اعطه", "وعطه", "الشغفوله", "امطار", "حي", "فيه", "توصيل",
    "اني", "ياغذي", "السلام", "التوصيل", "مغوار", "مندوب", "طلب", "طلبية"
]

# تعريف وتسجيل دخول البوت بالتوكن مباشرة بدون مشاكل start
client = TelegramClient('session_name', API_ID, API_HASH)

async def resolve_subscribers():
    resolved_ids = []
    for username in SUBSCRIBERS_USERNAMES:
        try:
            user = await client.get_entity(username)
            resolved_ids.append(user.id)
        except Exception as e:
            print(f"تعذر جلب المعرف {username}: {e}")
    return resolved_ids

@client.on(events.NewMessage(incoming=True))
async def monitor_groups(event):
    if event.is_group or event.is_channel:
        text = event.raw_text or ""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in KEYWORDS):
            sender = await event.get_sender()
            sender_name = getattr(sender, 'first_name', 'مستخدم')
            sender_username = getattr(sender, 'username', None)
            
            chat = await event.get_chat()
            chat_title = getattr(chat, 'title', 'مجموعة')
            
            alert_text = (
                f"🚨 <b>طلب جديد تم رصده 🔍</b>\n\n"
                f"👤 <b>المنسق:</b> {sender_name}\n"
                f"📍 <b>القروب:</b> {chat_title}\n\n"
                f"📝 <b>النص:</b>\n{text}"
            )
            
            button_url = f"https://t.me/{sender_username}" if sender_username else None
            
            subscribers_ids = await resolve_subscribers()
            for chat_id in subscribers_ids:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {
                    "chat_id": chat_id,
                    "text": alert_text,
                    "parse_mode": "HTML"
                }
                if button_url:
                    payload["reply_markup"] = {
                        "inline_keyboard": [[{"text": "📨 فتح المحادثة", "url": button_url}]]
                    }
                try:
                    requests.post(url, json=payload)
                except Exception as e:
                    print(f"خطأ في إرسال الإشعار: {e}")

# سيرفر وهمي لإرضاء موقع Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_web, daemon=True).start()

# تشغيل البوت باستخدام التوكن مباشرة
with client:
    client.run_until_disconnected()
