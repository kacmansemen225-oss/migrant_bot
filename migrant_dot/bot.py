import requests
import time

# 🔑 ВСТАВЬТЕ СВОЙ ТОКЕН СЮДА
TOKEN = "887479683:AAFBDAA_aMD80YE04Y1ITB1UUA_MOArnwB3J"

# 📋 Ваш ID
ADMIN_ID = 1222595258

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def send_keyboard(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    keyboard = {
        "keyboard": [
            ["📞 Хочу консультацию", "📄 Получить чек-лист"]
        ],
        "resize_keyboard": True
    }
    data = {"chat_id": chat_id, "text": text, "reply_markup": keyboard}
    requests.post(url, json=data)

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url, params={"timeout": 10, "offset": offset})
    data = response.json()
    if "result" in data:
        return data["result"]
    return []

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