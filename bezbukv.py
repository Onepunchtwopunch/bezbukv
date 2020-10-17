import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

import telebot



def is_working_with_bezbukv(word):
    a = []
    for x in word.lower():
        a.append(bool(x in "йцукенгшщзхъфывапролджэячсмитьбю *$"))
    return all(a)
bot = telebot.TeleBot('token_from_telega')
def get_page_soup(url):
    """открывает страницу и считывает html код"""
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    result = requests.get(url, headers)
    soup = BeautifulSoup(result.text)
    return soup
page_size = 20
pageboard0 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("/done")
pageboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("/next").add("/done")
pageboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("/previous", "/next").add("/done")
pageboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("/previous").add("/done")
soup = None
page = 0
lis = []
mw = None
@bot.message_handler(commands=["start"])
def s(message):
    bot.send_message(message.chat.id, "hello")
@bot.message_handler(commands=["changePageSize"])
def changeNumOfElemsInPage(message):
    global page_size
    r = message.text.strip()[16:].strip()
    if r:
        try:
            page_size = int(r)
            bot.send_message(message.chat.id, "длинна страниц установлена")
            return None
        except: pass
    bot.send_message(message.chat.id, "введите число после команды")
@bot.message_handler(commands=["done"])
def done(message):
    bot.delete_message(message.chat.id, message.message_id)
@bot.message_handler(commands=["next"])
def next_page(message):
    global page_size, pageboard2, pageboard3, page, lis, mw
    bot.delete_message(message.chat.id, message.message_id)
    page += 1
    k = pageboard2
    if len(lis[(page*page_size)+1: ((page+1)*page_size)+1]) < page_size: k = pageboard3
    bot.delete_message(mw.chat.id, mw.message_id)
    mw = bot.send_message(message.chat.id, ", ".join(lis[(page*page_size):((page+1)*page_size)+1]), reply_markup=k)
@bot.message_handler(commands=["previous"])
def previous_page(message):
    global page_size, pageboard1, pageboard2, page, lis, mw
    bot.delete_message(message.chat.id, message.message_id)
    page -= 1
    k = pageboard2
    if page <= 0: k = pageboard1
    bot.delete_message(mw.chat.id, mw.message_id)
    mw = bot.send_message(message.chat.id, ", ".join(lis[(page*page_size):((page+1)*page_size)+1]), reply_markup=k)
@bot.message_handler(content_types=["text"])
def action(message):
    global page_size, pageboard0, pageboard1, pageboard2, pageboard3, soup, page, lis, mw
    if is_working_with_bezbukv(message.text):
        soup = get_page_soup(f"https://bezbukv.ru/mask/{message.text.lower()}")
        lis = [_.text.strip().partition(".\n\t")[2] for _ in soup.find_all("div", class_="view")]
        if lis[(page+1*page_size):((page+2)*page_size)] == []: k = pageboard0
        else: k = pageboard1
        mw = bot.send_message(message.chat.id, ", ".join(lis[(page*page_size):((page+1)*page_size)]), reply_markup=k)
    else:
        bot.send_message(message.chat.id, "напишите на русском без специальных символов кроме $ и *")




bot.polling()

