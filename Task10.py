import telebot
import random
from mytoken import token

print('bot start')

HELP = """Добро пожаловать в Telegram bot DVZ
/help - справка по командам,
/add - добавить задачу в список (название задачи запрашиваем у пользователя),
/list - печать всего списка зажач за весь период наблюдения,
/show or /print - вывод списка задач,
/random - добавлять случайную задачу на дату сегодня,
/exit - выход из программы"""

RANDOM_TASKS = ["Пройти курс Pyton", "Написать Гвидо письмо","Помыть колеса","Погулять с Собакой"]

bot = telebot.TeleBot(token)

tasks = {}

def add_todo(date,task):
  if date in tasks:
  #Дата есть в словаре
    tasks[date].append(task)
  else:
  #Даты в словаре нет, тогда создаем с ключом дате
    tasks[date]=[]
    tasks[date].append(task)

def check_spacebar(message):#Подсчет количества пробелов в строке
    counter=0
    space = " "
    for text in message:
        if space in text:
            counter +=1
    return counter

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add"])
def add(message):
    spacebars=check_spacebar(message.text) #Контроль ввода даты и задачи, иначе бот вылетает, т.к. не находит значений command[1] и command[2]
    if spacebars > 1:
        command=message.text.split(maxsplit=2)
        date=command[1].lower() #Делаем все буквы в нижнем регистре
        task=command[2]
        add_todo(date,task)
        text="Задача " + task + " Добавлена на дату " + date
        bot.send_message(message.chat.id, text)
    else:
        promt_message="В команде /add не указаны date и task"
        bot.send_message(message.chat.id, promt_message)

@bot.message_handler(commands=["random"])
def random_add(message):
    date="сегодня"
    task=random.choice(RANDOM_TASKS)
    add_todo(date,task)
    text="Задача " + task + " Добавлена на дату " + date
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["show", "print"])
def show(message): #message = /show date
    spacebars=check_spacebar(message.text) #Контроль ввода даты иначе бот вылетает, т.к. не находит значений command[1]
    if spacebars > 0:
        command= message.text.split(maxsplit=1)
        date=command[1].lower()
        text=""
        if date in tasks:
            text = date.upper()+"\n"
            for task in tasks[date]:
                text = text + "- " +task + "\n"
        else:
            text="На эту дату ничего не назначено"
        bot.send_message(message.chat.id, text)
    else:
        promt_message="В команде /show не указанa date"
        bot.send_message(message.chat.id, promt_message)

@bot.message_handler(commands=["list"])
def mylist(message):
    text_date = ""
    for date in tasks:
        text_date = date.upper() + "\n"
        bot.send_message(message.chat.id, text_date)
        text_task = ""
        for text_task in tasks[date]:
            text_task = "- " +text_task + "\n"
            bot.send_message(message.chat.id, text_task)

bot.polling(none_stop=True) # none_stop - работает без остановки даже если получит ошибку