from random import randint
from urllib.parse import quote_plus
import pandas
import requests
from telebot import TeleBot, types
import random
import threading
from datetime import datetime
import time
import Test2

BOTAPI = '8310952722:AAFru9IGpWJOjygWUNxdQBCoYBVRfUAHwtA'

bot = TeleBot(BOTAPI)



users = set()

days_of_week ={
    1:"Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье",
}

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_sticker(m.chat.id, "CAACAgIAAxkBAAEPwBdpEqiSxlRd_H20g8brjTsUU9nWFAACBQADwDZPE_lqX5qCa011NgQ")
    bot.send_message(m.chat.id,
                     "🌟 Добро пожаловать! 🌟\n"
                     "Я - Бот очень очень очень крутого чела.\n"
                     "📖 Для списка команд используй /info")



@bot.message_handler(commands=['info'])
def info(m):
    kb1 = types.InlineKeyboardMarkup()
    kb2 = types.ReplyKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("/notice", callback_data="notice")
    btn2 = types.InlineKeyboardButton("/unsub", callback_data="unsub")
    btn3 = types.InlineKeyboardButton("/image",callback_data="image")
    btn4 = types.InlineKeyboardButton("/parser", callback_data="parser")

    btn5 = types.KeyboardButton("/notice")
    btn6 = types.KeyboardButton("/unsub")
    btn7 = types.KeyboardButton("/image")
    btn8 = types.KeyboardButton("/parser")

    kb1.add(btn1, btn2, btn3, btn4)
    kb2.add(btn5, btn6, btn7, btn8)

    bot.send_message(m.chat.id, "Список команд😇", reply_markup=kb1)
    bot.send_message(m.chat.id, "/start - привествие\n"
                                "/info - меню бота\n"
                                "/notice - подписаться на уведомления\n"
                                "/unsub - отписаться от уведомлений\n"
                                "/image - создание изображений\n"
                                "/parser - подборка товаров с DNS", reply_markup=kb2)

@bot.message_handler(commands=["notice"])
def notice(m):
    users.add(m.chat.id)
    bot.send_message(m.chat.id, "Вы подписались на уведомления✅")

@bot.message_handler(commands=["unsub"])
def unsub(m):
    users.discard(m.chat.id)
    bot.send_message(m.chat.id, "Вы отписались от уведомления❌")
def setNotification(user):
    today_weekday = datetime.today().weekday() + 1 #день недели в цифре 1-7

    if today_weekday == 6 or today_weekday == 7:
        bot.send_message(user, "Сегодня выходной. Занятий - НЕТ")

    # ! ФАЙЛ ЭКСЕЛЬ С ТАБЛИЦЕЙ
    df = pandas.read_excel("shedule.xlsx") #Эксель файл
    # ! ФАЙЛ ЭКСЕЛЬ С ТАБЛИЦЕЙ

    #все строки с расписанием на today weekday
    today_schedule = df[df['День'] == today_weekday]
    responce = f"Расписание на {days_of_week[today_weekday]}"
    for _, row in today_schedule.iterrows():
        responce += "▫️" * 20 + "\n"

        for column, value in row.items():
            if column != 'День' and pandas.notna(value) and str(value).strip() != '':
                column_name = column
                responce += f"{column_name}: {value}\n"

        responce += "\n" + "═" * 30 + "\n\n"

    total_lessons = len(today_schedule)
    responce += f"📊 Всего уроков: {total_lessons}"

    bot.send_message(user, responce)
def check_time():
    while True:
        now = datetime.now()
        if now.hour == 19 and now.minute ==50:
            for user in list(users):

                setNotification(user)
            time.sleep(60)
        else:
            time.sleep(30)
@bot.message_handler(commands=['image'])
def sendImg(m):
    prompt = m.text.partition(' ')[2].strip() #чисты запрос после пробела
    bot.send_message(m.chat.id, "Генерирую...")
    #генерим рандомное число
    seed = random.randint(0, 2_000_000_000)
    # улучшение запроса
    q = quote_plus(f"{prompt}, high quality, very detailed, soft light")

    url = f"https://image.pollinations.ai/prompt/{q}?width=500&height=500&seed={seed}&n=1"
    res = requests.get(url, timeout=90, allow_redirects=True)
    bot.send_photo(m.chat.id, res.content)
@bot.message_handler(commands=['parser'])
def parser(m):
    prompt = m.text.partition(' ')[2].strip()
    result = Test2.dns_search_uc(prompt)
    bot.send_message(m.chat.id, result)

def notification():
    scheduler_thread = threading.Thread(target=check_time)
    scheduler_thread.daemon = True  # фоновый поток
    scheduler_thread.start()

if __name__ == "__main__":
    print("Бот запущен...")
    notification()              # Запуск фоновых уведомлений
    bot.polling(none_stop=True)    # Основной цикл бота









