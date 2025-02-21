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

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton("Профиль")
item2 = types.KeyboardButton("Анонс мероприятия")
item3 = types.KeyboardButton("Публикация")
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
    item4 = types.KeyboardButton("Тест")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Здравствуйте, я бот ArdBot. Для управления используйте клавиатуру.", reply_markup=markup)
@bot.message_handler(commands=["start"])
def welcome(message):
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Здравствуйте, я бот ArdBot. Для управления используйте клавиатуру.", reply_markup=markup)
@bot.message_handler(content_types=["text"])
def menu(message):
    if message.chat.type == "private":
        if message.text == "Тест":
            test1 = bot.send_message(message.chat.id, "Тест")
            bot.register_next_step_handler(test1, test2)
        elif message.text == "аш":
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
            if str(message.chat.id) in str(datebase.new_user_id):
                bot.send_message(message.chat.id, "У вас уже есть аккаунт!")
                markupc = types.ReplyKeyboardMarkup(resize_keyboard=True)
                itemc1 = types.KeyboardButton("Изменить профиль")
                itemc2 = types.KeyboardButton("Вернуться обратно")
                markupc.add(itemc1, itemc2)
                bot.send_message(message.chat.id, "Выберите комманду:", reply_markup=markupc)
                bot.send_message(message.chat.id, "Здесь распологается информация о вашей учетной записи: " + "\nВаше имя:" + (str(datebase.new_user_name))+ "\nВаш ID сессии: "+ (str(datebase.new_user_id)) + "\nВаша дата: " + (str(datebase.new_user_data)), reply_markup=markupc)
                bot.send_message(message.chat.id, "Выберите комманду: ")
            else:
                name_bot = bot.send_message(message.chat.id, "Раздел в разработке.")
                bot.register_next_step_handler(name_bot, name_name)
        elif message.text == "sk":
            bot.send_message(message.chat.id, "Бот остановлен.")
            logger.error("Bot stop polling.")
            bot.stop_polling()
        elif message.text == "Изменить профиль":
            markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_1_1 = types.KeyboardButton("Изменить количество мероприятий")
            item_1_2 = types.KeyboardButton("Вернуться обратно")
            markup1.add(item_1_1, item_1_2)

            namere = bot.send_message(message.chat.id, "Комманды для смены профиля: ", reply_markup=markup1)

            bot.register_next_step_handler(namere, rename)
        elif message.text == "Вернуться обратно":
            back = bot.send_message(message.chat.id, "Введите еще раз")
            bot.register_next_step_handler(back, welcome)
        else:
            markup.add(item1, item2, item3)
            
            bot.send_message(message.chat.id, "Неизвестная комманда", reply_markup=markup)
def test2(message):
    try:
        bot.send_message(message.chat.id, "коопо: "+ str(datebase.test))
        datebase.test.append(message.text)
        bot.send_message(message.chat.id, "коопо: "+ str(datebase.test))
    except Exception as e:
        bot.send_message(message.chat.id, "errror")
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
def name_data(message):
    try:
        user_name1 = message.text
        datebase.new_user_id.append(str(message.chat.id))
        datebase.new_user_name.append(str(user_name1))
        bot.send_message(message.chat.id, "Ваше имя:" + (str(datebase.new_user_name)))
        user_n_data = bot.send_message(message.chat.id, "Введите дату рождения: ")
        bot.register_next_step_handler(user_n_data, user_n1_data)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка 4")   
def user_n1_data(message):
    try:
        user_data1 = message.text
        datebase.new_user_data.append(str(user_data1))
        
        bot.send_message(message.chat.id, "Ваша дата:" + (str(datebase.new_user_name))+ "\nВаш ID сессии: "+ (str(datebase.new_user_id)) + "\nВаша дата: " + (str(datebase.new_user_data)))
        bot.send_message(message.chat.id, "Нажмите снова `Профиль`")
        print(datebase.new_user_id, datebase.new_user_name, datebase.new_user_data)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка")
def name_name(message):
    try:
        if str(message.chat.id) in datebase.new_user_id:
            bot.send_message(message.chat.id, "У вас уже есть аккаунт!")
            markupc = types.ReplyKeyboardMarkup(resize_keyboard=True)
            bot.send_message(message.chat.id, "Ваш профиль:" + "\nВаше имя: "+ datebase.new_user_name + "\nВаша дата рождения: " + datebase.new_user_data + "ID вашей сессии: "+ datebase.new_user_id)
            itemc1 = types.KeyboardButton("Изменить профиль")
            itemc2 = types.KeyboardButton("Вернуться обратно")
            markupc.add(itemc1, itemc2)
            bot.send_message(message.chat.id, "Выберите комманду:", reply_markup=markupc)
        else:
            name_name1 = bot.send_message(message.chat.id, "Введите ваше имя: ")
            bot.register_next_step_handler(name_name1, name_data)
            
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка 3")  
#Изменение профиля
def rename(message):
    try:
        bot.send_message(message.chat.id, "щдфыва")
        if message.text == "Изменить количество мероприятий":
            bot.send_message(message.chat.id, "230к")
    except Exception as e:
        bot.send_message(message.chat.id, "щдфыв1а")
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
