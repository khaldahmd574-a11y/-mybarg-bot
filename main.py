import os
from telethon import TelegramClient, events
import requests

API_ID = 39120728
API_HASH = '1deec8393ce5aa05c54c0c7e280377d4'
BOT_TOKEN = '8782796916:AAGKs4vgK6s302vNpRAJ_3lU0YwjOHR0ybA'

SUBSCRIBERS_USERNAMES = [
    "abood1317",
    "shaybq",
    "Waaaaaaa33"
]

KEYWORDS = [
    "جيزان", "جازان", "ضمد", "صبيا", "خضيره", "رديس", "القمري",
    "الدرب", "صامطه", "مزهره", "المضايا", "الحقل", "بيت الرومنسي",
    "البيك", "الخضراء", "الطوال", "المضايا", "الراشد", "ماك", "كادي", "المجمع",
    "محليه", "لمحليه", "مخطط", "احتاج", "ابغى", "ابغا", "مين",
    "يرجعني", "يجيب", "يوصل", "توصل", "يروح", "تروح", "ابتسام",
    "الزاكي", "راجع", "راجعه", "بيش", "السوق", "دوامات", "يلتزم",
    "اعطيه", "رعشه", "الشعفوليه", "المطار", "حي", "فيه", "توصيل",
    "الي", "ياخذني", "السلام", "توصيل", "مشوار", "مندوب", "طلب", "طلبية"
]

client = TelegramClient('session_name', API_ID, API_HASH)

async def resolve_subscribers():
    resolved_ids = []
    for username in SUBSCRIBERS_USERNAMES:
        try:
            user = await client.get_entity(username)
            resolved_ids.append(user.id)
        except Exception as e:
            print(f"تعذر جلب أيدي المعرف {username}: {e}")
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
                f"📩 <b>طلب جديد تم رصده:</b>\n\n"
                f"👤 <b>العضو:</b> {sender_name}\n"
                f"📍 <b>القروب:</b> {chat_title}\n\n"
                f"💬 <b>النص:</b>\n{text}"
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
                        "inline_keyboard": [[{"text": "📬 فتح المحادثة", "url": button_url}]]
                    }
                try:
                    requests.post(url, json=payload)
                except Exception as e:
                    print(f"خطأ في إرسال البوت للمشترك: {e}")

print("جاري تشغيل نظام رصد وتوزيع الطلبات...")
client.start()
client.run_until_disconnected()

