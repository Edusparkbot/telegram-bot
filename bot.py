from flask import Flask, request
import telebot
import os
import openai

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = "https://flowersmakinsk.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

@server.route('/')
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook set", 200

@server.route(f'/{BOT_TOKEN}', methods=['POST'])
def receive_update():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'OK', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('📦 Оформить заказ', '⭐ Отзывы')
    markup.row('💰 Прайс-лист', '🤖 AI помощник')
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите опцию:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '📦 Оформить заказ':
        bot.send_message(message.chat.id, "Напишите, какие цветы вы хотите заказать 💐")
    elif message.text == '⭐ Отзывы':
        bot.send_message(message.chat.id, "Отзывы можно посмотреть на нашем сайте или в Instagram 🌟")
    elif message.text == '💰 Прайс-лист':
        bot.send_message(message.chat.id, "💐 Розы — 800₸\n🌷 Тюльпаны — 600₸\n🌻 Подсолнухи — 700₸")
    elif message.text == '🤖 AI помощник':
        bot.send_message(message.chat.id, "Напишите свой вопрос, и AI постарается помочь 🤖")
    elif OPENAI_API_KEY:
        try:
            openai.api_key = OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message.text}]
            )
            reply = response.choices[0].message.content.strip()
            bot.send_message(message.chat.id, reply)
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Ошибка AI: {e}")
    else:
        bot.send_message(message.chat.id, "AI временно недоступен. Попробуйте позже.")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)