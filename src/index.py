import requests
import random
import telebot
from telebot import types
import time
from app.Confs.TgApiConf import TgApiConf
from app.Confs.TgConf import TgConf
from app.Services.VideoPost import Video
from app.Services.PhotoPost import Photo
from app.Reposytories.SubcsribersRepository import Subscribers
from app.Reposytories.BlackListRepository import BlackList
from app.Reposytories.PostRepository import PostRepository

bot = telebot.TeleBot(TgApiConf.token)
Photo = Photo(bot)
Video = Video(bot)
SubscribersRepository = Subscribers()
BlacklistRepository = BlackList()
PostRep = PostRepository()
Https = TgApiConf.https

print("Start")

global posts, videoPosts, canSendFoto, canSendVideo
file = open("app/countPostsVideo.txt", "r")
videoPosts = int(file.read())
file.close()
file = open("app/countPosts.txt", "r")
posts = file.read()
file.close()
canSendFoto = False
canSendVideo = False

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Случайное фото")
btn2 = types.KeyboardButton("Загрузить фото")
btn3 = types.KeyboardButton("Случайное видео")
btn4 = types.KeyboardButton("Загрузить видео")
markup.add(btn1, btn2, btn3, btn4)


def waitPay(userId, billid, sekretKey, message):
    zaprosURL = "https://api.qiwi.com/partner/bill/v1/bills/" + billid
    count = 0
    while True:
        time.sleep(10)
        count += 1
        if (count == 50):
            break
        zapros = requests.get(zaprosURL,
                              headers={"Authorization": "Bearer " + sekretKey, "Accept": "application/json"}).json()
        if (zapros['status']['value'] == "WAITING"):
            print(str(userId) + " оплачивает подписку, ждем...")
        elif (zapros['status']['value'] == "PAID"):
            print(str(userId) + " оплатил счет!")
            PayResult(message)


def CheckSubscriber(userId):
    result = False
    user = SubscribersRepository.getUser(userId=userId)
    if user is not None:
        currentTime = round(time.time())
        if user[SubscribersRepository.field_end > currentTime]:
            result = True
    return result


def CheckBlackList(userId):
    result = True
    if BlacklistRepository.getUser(userId=userId) is not None:
        result = False
    return result


def sendPhoto(message, posts, canSendFoto):
    try:
        PostId = int(random.randint(12, int(posts)))
        curTime = time.time()
        curTime = time.gmtime(curTime + (60 * 60 * 3))
        curTime = time.strftime("%H:%M:%S", curTime)
        print(str(message.from_user.username) + " (" + str(message.from_user.id) + ")-" + str(
            curTime) + "//ID фото-поста - " + str(PostId) + ", последний ID - " + str(posts))
        bot.copy_message(userId, "@RandomFotoChannel", PostId, "")
        canSendFoto = False
    except:
        sendPhoto(message, posts, canSendFoto)


def sendVideo(message, videoPosts, canSendVideo):
    try:
        PostId = random.randint(2, videoPosts)
        curTime = time.time()
        curTime = time.gmtime(curTime + (60 * 60 * 3))
        curTime = time.strftime("%H:%M:%S", curTime)
        print(str(message.from_user.username) + " (" + str(message.from_user.id) + ")-" + str(
            curTime) + "//ID видео-поста - " + str(PostId) + ", последний ID - " + str(videoPosts))
        bot.copy_message(userId, "@RandomniyVidoeChannel", PostId, "")
        canSendVideo = False
    except:
        sendVideo(message, videoPosts, canSendVideo)


@bot.message_handler(commands=["start"])
def HelloMess(message):
    global userId, UserName, canSendFoto, canSendVideo
    canSendFoto = False
    canSendVideo = False
    UserName = "@" + str(message.from_user.username)
    file = open("app/UsersNames.txt", "r")
    count = 0
    for line in file:
        line = line.replace("\n", "")
        if (line == UserName):
            count += 1
    file.close()
    if (count == 0):
        file = open("app/UsersNames.txt", "a")
        file.write(UserName + "\n")
    file.close()
    userId = message.from_user.id
    bot.send_message(userId, "Привет, " + message.from_user.first_name)
    bot.send_message(message.chat.id, text="Жми на кнопку чтобы увидеть рандомную фотку или загрузить свою!",
                     reply_markup=markup)


@bot.message_handler()
def Handler(message):
    global userId, canSendFoto, canSendVideo
    userId = message.from_user.id
    resultBlacklistCheck = CheckBlackList(message.from_user.id)
    if not resultBlacklistCheck:
        bot.send_message(userId, "вы забанены(")
    else:
        if message.text == "Случайное фото":
            Photo.send(message, posts, canSendFoto)
        elif message.text == "Загрузить фото":
            canSendFoto = True
            bot.send_message(userId, "Тогда отправь мне фото")
        elif message.text == "Случайное видео":
            if CheckSubscriber(str(message.from_user.id)) or userId in TgConf.admins:
                sendVideo(message, videoPosts, canSendVideo)
            else:
                bot.send_message(userId, "Время вашей подписки вышло или вы не были подписаны ранее")
                submarkup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                    types.KeyboardButton("Купить"),
                    types.KeyboardButton("В другой раз")
                )
                bot.send_message(userId,
                                 message.from_user.first_name + ", для просмотра видео тебе необходимо оформить подписку.\nПодписка стоит 70 рублей в месяц, после чего ее снова потребуется продлить. Возврат средств за оформление подписки не проводится.\nНу так что, хочешь?",
                                 reply_markup=submarkup)
        elif (message.text == "Загрузить видео"):
            canSendVideo = True
            bot.send_message(userId, "Тогда отправь мне видео")
        elif (message.text == "Да"):
            types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                types.KeyboardButton("Оплата через Телеграмм"),
                types.KeyboardButton("Я передумал"))
        elif (message.text == "Нет" or message.text == "Я передумал"):
            bot.send_message(userId, "Как хочешь, " + message.from_user.first_name + ")", reply_markup=markup)
        elif (message.text == "Qiwi"):
            billid = random.randint(100, 10000000)
            sekretKey = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6IjRuNmFycy0wMCIsInVzZXJfaWQiOiI3OTY3MTAxOTM2MSIsInNlY3JldCI6ImIwOWJlOTQ5ODE2NGYyYTI0Yzg3NTEyODUzYmNkMzVjZDUwZjkzNjZjNmI1NTA5ZjgxZDM0NmZmMGY2MjJhNzMifX0="
            zaprosURL = "https://api.qiwi.com/partner/bill/v1/bills/" + str(billid)
            curTime = time.time()
            tomorrowTime = curTime + (60 * 5)
            tomorrowTime = time.gmtime(tomorrowTime)
            tomorrowTime = time.strftime("%Y-%m-%dT%H:%M:%S+03:00", tomorrowTime)
            zapros = requests.put(zaprosURL, json={"amount": {"value": "70.00", "currency": "RUB"},
                                                   "expirationDateTime": tomorrowTime,
                                                   "customFields": {"themeCode": "Enryke-VIHiGDGElf", "tgID": userId}},
                                  headers={"Authorization": "Bearer " + sekretKey, "Content-Type": "application/json",
                                           "Accept": "application/json"}).json()
            bot.send_message(userId, "Отлично! Перейди по ссылке ниже и оплати")
            bot.send_message(userId, zapros['payUrl'])
            waitPay(userId, str(billid), sekretKey, message)


@bot.message_handler(content_types=['photo'])
def saveFoto(message):
    global posts, canSendFoto
    print(str(message.from_user.username) + "//Состояние в saveFoto - " + str(canSendFoto))
    userId = message.from_user.id
    if (canSendFoto == True):
        posts = int(posts)
        posts += 1
        zapros = requests.post(Https + "/CopyMessage", data={'chat_id': "@RandomFotoChannel", 'from_chat_id': userId,
                                                             'message_id': message.message_id,
                                                             "caption": str(posts)}).json()
        file = open("app/countPosts.txt", "w")
        file.write(str(posts))
        file.close()
        canSendFoto = False
        bot.send_message(userId, "Спасибо за пополнение коллекции бота!")
    elif (canSendFoto == False):
        bot.send_message(userId, "Сначала нажми на кнопку 'Загрузить свою фотку'")


@bot.message_handler(content_types=['video'])
def saveVideo(message):
    global videoPosts, canSendVideo
    print(str(message.from_user.username) + "//Состояние в saveVideo - " + str(canSendVideo))
    userId = message.from_user.id
    if (canSendVideo == True):
        videoPosts = videoPosts
        videoPosts += 1
        zapros = requests.post(Https + "/CopyMessage",
                               data={'chat_id': "@RandomniyVidoeChannel", 'from_chat_id': userId,
                                     'message_id': message.message_id, "caption": str(videoPosts)}).json()
        file = open("app/countPostsVideo.txt", "w")
        file.write(str(videoPosts))
        file.close()
        canSendVideo = False
        bot.send_message(userId, "Спасибо за пополнение коллекции бота!")
    elif (canSendVideo == False):
        bot.send_message(userId, "Сначала нажми на кнопку 'Загрузить свою фотку'")


def PayResult(message):
    month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    secInDay = 60 * 60 * 24
    CurrentTime = time.localtime(time.time())
    InMonth = round(time.time() + secInDay * month[CurrentTime.tm_mon])
    subscriberId = message.from_user.id
    file = open("app/Subscribers.txt", "a")
    file.write(str(subscriberId) + " " + str(InMonth) + "\n")
    file.close()
    bot.send_message(subscriberId,
                     "Поздравляю," + message.from_user.username + ", вы оформили подписку на месяц для возможности просматривать рандомные видео, спасибо что поддержал разработчика!)",
                     reply_markup=markup)


print("Started")
bot.infinity_polling()
