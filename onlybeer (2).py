import telebot
import configonl
import datetime
import datebase
import os
from telebot import types
from loguru import logger

bot = telebot.TeleBot(configonl.TOKEN)

# Хранилище данных (временное, лучше использовать БД)
user_data = {}
data_base = {}
data_id = ""
data_time = ()
time_data = (datetime.datetime.now().time())
user_name = {}
os.system('cls' if os.name == 'nt' else 'clear')
print(configonl.icon)
print(configonl.icon2)

@bot.message_handler(commands=["start"])
def handler_new_member(message):
    print("New user!")
    data_base[data_id] = {"data_id:": message.from_user.username}
    data_base[data_id][data_time] = {"data_time: ": time_data}
    print(data_base[data_id])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Профиль")
    item2 = types.KeyboardButton("Анонс мероприятия")
    item3 = types.KeyboardButton("Публикация")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Здравствуйте, я бот ArdBot. Для управления используйте клавиатуру.", reply_markup=markup)
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
        if message.text == "аш":
            logger.info("Попытка получения доступа к админу" + str(message.chat.id))
            if str(message.chat.id) in datebase.user_admins:
                start_adm = bot.send_message(message.chat.id, "Введите y: ")

                bot.register_next_step_handler(start_adm, adm_start)
            else:
                bot.send_message(message.chat.id, "Вам отказано доступе!")
        elif message.text == "те":
            new_dictionary = bot.send_message(message.chat.id, "Ведите значение: ")
        elif message.text == "Публикация":
            bot.send_message(message.chat.id, "Здесь вы можете прислать новость для публикации (ваше мероприятия, фотографии и в целом ваши эмоции от мероприятия): ")
            msg1 = bot.send_message(message.chat.id, "Ваедите название мероприятия (заголовок):")
            bot.register_next_step_handler(msg1, new_event)
        elif message.text == "Анонс мероприятия":
            bot.send_message(message.chat.id, "Введите характеристики мероприятия:")
            msg = bot.send_message(message.chat.id, "Дата мероприятия (ДД.ММ.ГГГГ):")
            bot.register_next_step_handler(msg, process_date)
        elif message.text == "Профиль":
            bot.send_message(message.chat.id, "Раздел в разработке.")

            name_bot = bot.send_message(message.chat.id, "Введите ваше имя: ")
            bot.register_next_step_handler(name_bot, name_name)
        elif message.text == "sk":
            bot.send_message(message.chat.id, "Бот остановлен.")
            logger.error("Bot stop polling.")
            bot.stop_polling()
        else:
            bot.send_message(message.chat.id, "Неизвестная комманда")

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
    logger.info(f"New publication: {user_data[user_id]}")
#Профиль------------------
def name_name(message):
    try:
        if str(message.chat.id) in datebase.user:
            bot.send_message(message.chat.id, "Собалезную")
        else:
            user_id = message.from_user.id
            user_name[user_id] = {"user_name:": message.text}
            bot.send_message(message.chat.id, "Ваше имя:" + str(user_name[user_id]))
            user_n_data = bot.send_message(message.chat.id, "Введите дату рождения: ")
            bot.register_next_step_handler(user_n_data, user_n1_data)
            logger.info(f"Новый пользователь:\n"+ str(user_name[user_id]))
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка 3")     
def user_n1_data(message):
    try:
        user_id = message.from_user.id
        user_data[user_id] = {"Дата пользователя": message.text}
        bot.send_message(message.chat.id, "Ваша дата:" + str(user_data[user_id]) + "\nВаше имя"+ str(user_name[user_id]))
        logger.info("Новый пользователь: " + str(user_name[user_id]) + str(user_data[user_id]))
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка")
#Админка--------------------
def adm_start(message):
    try:
        bot.send_message(message.chat.id, "Тест")
        markup_adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_admin = types.KeyboardButton("Добавление значения к мероприятию")
        item_admin1 = types.KeyboardButton("Вторая строка")
        markup_adm.add(item_admin, item_admin1)
        bot.send_message(message.chat.id, "Вы успешно получили доступ к командам администратора", reply_markup=markup_adm)
        bot.send_message(message.chat.id, message.from_user.id)
        if message.text == "Добавление значения к мероприятию":
            named_ivent = bot.send_message(message.chat.id, "Введите название нового мероприятия: ")
            bot.register_next_step_handler(named_ivent, ivent_named)
        else:
            bot.send_message(message.chat.id, "Ошибка2")
    except Exception as e:
        bot.send_message(message.chat.id, "Неизвестная ошибка")
def ivent_named(message):
    try:
        data_name = message.text
        bot.send_message(message.chat.id, "Успешно "+str(data_name)+ "создано")
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка")
bot.infinity_polling()
