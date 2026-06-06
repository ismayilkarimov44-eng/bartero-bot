```python
import telebot
from telebot import types

TOKEN = "8890778895:AAHQNjQi0PCbn9341tN0c8DHTffmqObw3Zo"
bot = telebot.TeleBot(TOKEN)

offers = []

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📦 Предложить вещь', '🔍 Смотреть предложения')
    bot.send_message(message.chat.id,
        "👋 Добро пожаловать в Bartero!\n\nЗдесь вы можете обменять ненужные вещи на нужные.\n\nВыберите действие:",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📦 Предложить вещь')
def offer_item(message):
    bot.send_message(message.chat.id, "Напишите что вы предлагаете и что хотите взамен.\n\nПример: Предлагаю стул, хочу велосипед")
    bot.register_next_step_handler(message, save_offer)

def save_offer(message):
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    offers.append({
        'user': message.from_user.first_name,
        'username': username,
        'user_id': message.chat.id,
        'text': message.text
    })
    bot.send_message(message.chat.id, "✅ Ваше предложение добавлено! Люди увидят ваш контакт.")

@bot.message_handler(func=lambda m: m.text == '🔍 Смотреть предложения')
def show_offers(message):
    if not offers:
        bot.send_message(message.chat.id, "Пока нет предложений. Будьте первым!")
    else:
        for o in offers:
            bot.send_message(message.chat.id, f"👤 {o['user']} ({o['username']}):\n{o['text']}")

bot.polling()
```

После вставки нажми **"Внесите изменения"** 👇
