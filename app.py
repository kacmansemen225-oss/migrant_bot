 import os
import requests
import time
from flask import Flask
from threading import Thread

app = Flask(name)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID = 1222595258

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})

def send_keyboard(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    keyboard = {
        "keyboard": [["📞 Хочу консультацию", "📄 Получить чек-лист"]],
        "resize_keyboard": True
    }
    requests.post(url, json={"chat_id": chat_id, "text": text, "reply_markup": keyboard})

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url, params={"timeout": 10, "offset": offset})
    data = response.json()
    return data.get("result", [])

def bot_loop():
    print("✅ Бот запущен и слушает сообщения...")
    last_update_id = 0
    while True:
        updates = get_updates(last_update_id + 1)
        for update in updates:
            last_update_id = update["update_id"]
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                if text == "/start":
                    send_keyboard(chat_id, "🇷🇺 Здравствуйте! Я помощник по миграционным вопросам.\n\nВыберите действие:")
                elif text == "📞 Хочу консультацию":
                    send_message(chat_id, "Введите ваш номер телефона и имя:")
                elif text == "📄 Получить чек-лист":
                    send_message(chat_id, "📎 Список документов для РВП:\n\n1. Заявление\n2. Паспорт\n3. Миграционная карта\n4. Медсправка\n5. Квитанция")
                else:
                    if text and text not in ["/start", "📞 Хочу консультацию", "📄 Получить чек-лист"]:
                        send_message(ADMIN_ID, f"🆕 Новая заявка!\n\nКлиент: {text}")
                        send_message(chat_id, "✅ Спасибо! Юрист свяжется с вами.")
        time.sleep(1)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "OK"

if name == "main":
    thread = Thread(target=bot_loop)
    thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
