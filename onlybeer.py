import telebot
import configonl
import os
from telebot import types
from loguru import logger

bot = telebot.TeleBot(configonl.TOKEN)

# Хранилище данных (временное, лучше использовать БД)
user_data = {}
os.system('cls' if os.name == 'nt' else 'clear')
print(configonl.icon)
print(configonl.icon2)
@bot.message_handler(commands=["start"])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Профиль")
    item2 = types.KeyboardButton("Анонс мероприятия")
    item3 = types.KeyboardButton("Публикация")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Здравствуйте, я бот ArdBot. Для управления используйте клавиатуру.", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def menu(message):
    if message.chat.type == "private":
        if message.text == "Публикация":
            bot.send_message(message.chat.id, "Здесь вы можете прислать новость для публикации (ваше мероприятия, фотографии и в целом ваши эмоции от мероприятия): ")
            msg1 = bot.send_message(message.chat.id, "Ваедите название мероприятия (заголовок):")
            bot.register_next_step_handler(msg1, new_event)
        if message.text == "Анонс мероприятия":
            bot.send_message(message.chat.id, "Введите характеристики мероприятия:")
            msg = bot.send_message(message.chat.id, "Дата мероприятия (ДД.ММ.ГГГГ):")
            bot.register_next_step_handler(msg, process_date)
        elif message.text == "Профиль":
            bot.send_message(message.chat.id, "Раздел в разработке.")
        elif message.text == "sk":
            bot.send_message(message.chat.id, "Бот остановлен.")
            bot.stop_polling()

def process_date(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = {'date': message.text}
        msg = bot.send_message(message.chat.id, "Время мероприятия (ЧЧ:ММ):")
        bot.register_next_step_handler(msg, process_time)
    except Exception as e:
        logger.error(e)
        bot.reply_to(message, "Ошибка. Попробуйте снова.")

def process_time(message):
    try:
        user_id = message.from_user.id
        user_data[user_id]['time'] = message.text
        msg = bot.send_message(message.chat.id, "Количество участников:")
        bot.register_next_step_handler(msg, process_participants)
    except Exception as e:
        logger.error(e)
        bot.reply_to(message, "Ошибка. Попробуйте снова.")

def process_participants(message):
    try:
        user_id = message.from_user.id
        user_data[user_id]['participants'] = message.text
        msg = bot.send_message(message.chat.id, "Категория мероприятия:")
        bot.register_next_step_handler(msg, process_category)
    except Exception as e:
        logger.error(e)
        bot.reply_to(message, "Ошибка. Попробуй снова.")

def process_category(message):
    user_id = message.from_user.id
    user_data[user_id]['category'] = message.text
    bot.send_message(message.chat.id, "Анонс создан! Данные:\n" + str(user_data[user_id]))
    os.system('cls' if os.name == 'nt' else 'clear')
    print(icon)
    print(icon2)
    logger.info(f"New event: {user_data[user_id]}")
#Новый эвент---------------


def new_event(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = {'event_name': message.text}  # Сохраняем название мероприятия
        msg1 = bot.send_message(message.chat.id, "Введите описание мероприятия, свои впечатления, ссылки на фотографии (в формате телеграмма, ссылку на ваш TG): ")
        bot.register_next_step_handler(msg1, event_info)
    except Exception as e:
        logger.error(e)
        bot.reply_to(message, "Ошибка. Попробуй снова.")
        
def event_info(message):
    user_id = message.from_user.id
    user_data[user_id]['event_info'] = message.text  # Добавляем описание мероприятия в существующий словарь
    bot.send_message(message.chat.id, "Успешно подали заявку на публикацию!")
    bot.send_message(message.chat.id, "Анонс создан! Данные:\n" + str(user_data[user_id]))
    print(icon)
    print(icon2)
    os.system('cls' if os.name == 'nt' else 'clear')
    logger.info(f"New publication: {user_data[user_id]}")
bot.infinity_polling()