import telebot
from telebot import types

TOKEN = "8890778895:AAHQNjQi0PCbn9341tN0c8DHTffmqObw3Zo"
bot = telebot.TeleBot(TOKEN)

offers = []
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('📦 Предложить вещь', '🔍 Смотреть предложения')
    bot.send_message(message.chat.id,
        "👋 Добро пожаловать в Bartero!\n\nОбменяй ненужные вещи на нужные.\n\nВыберите действие:",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '📦 Предложить вещь')
def offer_item(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "📸 Отправьте фото вашей вещи:")
    bot.register_next_step_handler(message, get_photo)

def get_photo(message):
    if message.photo:
        user_data[message.chat.id]['photo'] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "✏️ Теперь напишите описание и что хотите взамен:\n\nПример: Велосипед, хочу телефон")
        bot.register_next_step_handler(message, get_description)
    else:
        bot.send_message(message.chat.id, "❌ Пожалуйста отправьте фото!")
        bot.register_next_step_handler(message, get_photo)

def get_description(message):
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    user_data[message.chat.id]['text'] = message.text
    user_data[message.chat.id]['username'] = username
    user_data[message.chat.id]['user'] = message.from_user.first_name
    offers.append(user_data[message.chat.id].copy())
    bot.send_message(message.chat.id, "✅ Объявление добавлено! Люди увидят ваш контакт.")

@bot.message_handler(func=lambda m: m.text == '🔍 Смотреть предложения')
def show_offers(message):
    if not offers:
        bot.send_message(message.chat.id, "Пока нет предложений. Будьте первым!")
    else:
        for o in offers:
            caption = f"👤 {o['user']} ({o['username']})\n{o['text']}"
            if 'photo' in o:
                bot.send_photo(message.chat.id, o['photo'], caption=caption)
            else:
                bot.send_message(message.chat.id, caption)

bot.polling()
