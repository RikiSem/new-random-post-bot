import telebot
from telebot import types
import time
from threading import Thread
from app.Confs.TgApiConf import TgApiConf
from app.Confs.TgConf import TgConf
from app.Services.VideoPost import Video
from app.Services.PhotoPost import Photo
from app.Repositories.SubcsribersRepository import Subscribers
from app.Repositories.BlackListRepository import BlackList
from app.Repositories.PostRepository import PostRepository
from app.Confs.BotButtons import BotButtons

bot = telebot.TeleBot(TgApiConf.token)
Photo = Photo(bot)
Video = Video(bot)
SubscribersRepository = Subscribers()
BlacklistRepository = BlackList()
PostRep = PostRepository()
Https = TgApiConf.https

print("Start")

global canSendFoto, canSendVideo
canSendFoto = False
canSendVideo = False
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(
    types.KeyboardButton(BotButtons.randomFoto),
    types.KeyboardButton(BotButtons.loadFoto),
    types.KeyboardButton(BotButtons.randomVideo),
    types.KeyboardButton(BotButtons.loadVideo),
)
submarkup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton(BotButtons.buy),
    types.KeyboardButton(BotButtons.cancel)
)
paymarkup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton(BotButtons.pay),
    types.KeyboardButton(BotButtons.cancel)
)


def checkSubscriber(userId):
    result = False
    user = SubscribersRepository.getUser(userId=userId)
    if user is not None:
        currentTime = round(time.time())
        if user[SubscribersRepository.field_end > currentTime]:
            result = True
    return result


def checkBlackList(userId):
    result = True
    if BlacklistRepository.getUser(userId=userId) is not None:
        result = False
    return result


@bot.message_handler(commands=["start"])
def firstStart(message):
    bot.send_message(message.from_user.id, "Привет, " + message.from_user.first_name, reply_markup=markup)


@bot.message_handler()
def handler(message):
    global canSendFoto, canSendVideo
    userId = message.from_user.id
    resultBlacklistCheck = checkBlackList(message.from_user.id)
    if not resultBlacklistCheck:
        bot.send_message(userId, "вы забанены(")
    else:
        if message.text == BotButtons.randomFoto:
            sendFotoThread = Thread(target=Photo.send(message))
            sendFotoThread.start()
        elif message.text == BotButtons.loadFoto:
            canSendFoto = True
            bot.send_message(userId, "Тогда отправь мне фото")
            canSendFoto = False
        elif message.text in [BotButtons.randomVideo, BotButtons.loadVideo]:
            if checkSubscriber(str(message.from_user.id)) or userId in TgConf.admins:
                if message.text == BotButtons.randomVideo:
                    sendVideoThread = Thread(target=Video.send(message))
                    sendVideoThread.start()
                else:
                    canSendVideo = True
                    bot.send_message(userId, "Тогда отправь мне видео")
                    canSendVideo = False
            else:
                bot.send_message(userId, "Время вашей подписки вышло или вы не были подписаны ранее")
                bot.send_message(userId,
                                 message.from_user.first_name + ", для просмотра видео тебе необходимо оформить подписку.\nПодписка стоит 70 рублей в месяц, после чего ее снова потребуется продлить. Возврат средств за оформление подписки не проводится.\nНу так что, хочешь?",
                                 reply_markup=submarkup)
        elif message.text == BotButtons.buy:
            bot.send_message(userId, "Оплата происходит через кошелек Телеграмм", reply_markup=paymarkup)
        elif message.text == BotButtons.cancel:
            bot.send_message(userId, "Как хочешь, " + message.from_user.first_name + ")", reply_markup=markup)
        elif message.text == BotButtons.pay:
            pass


@bot.message_handler(content_types=['photo'])
def saveFoto(message):
    global canSendFoto
    canSendFoto = True
    if canSendFoto:
        Photo.save(message)
        print(str(message.from_user.username) + "//Состояние в saveFoto - " + str(canSendFoto))
        bot.send_message(message.from_user.id, "Спасибо за пополнение коллекции бота!")
        canSendFoto = False
    elif not canSendFoto:
        bot.send_message(message.from_user.id, f"Сначала нажми на кнопку '{BotButtons.loadFoto}'")


@bot.message_handler(content_types=['video'])
def saveVideo(message):
    global canSendVideo
    canSendVideo = True
    if canSendVideo:
        Video.save(message)
        print(str(message.from_user.username) + "//Состояние в saveVideo - " + str(canSendVideo))
        bot.send_message(message.from_user.id, "Спасибо за пополнение коллекции бота!")
        canSendVideo = False
    elif not canSendVideo:
        bot.send_message(message.from_user.id, "Сначала нажми на кнопку 'Загрузить свою фотку'")


def payResult(message):
    month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    secInDay = 60 * 60 * 24
    CurrentTime = time.localtime(time.time())
    InMonth = round(time.time() + secInDay * month[CurrentTime.tm_mon])
    subscriberId = message.from_user.id
    bot.send_message(subscriberId,
                     "Поздравляю," + message.from_user.username + ", вы оформили подписку на месяц для возможности просматривать рандомные видео, спасибо что поддержал разработчика!)",
                     reply_markup=markup)


print("Started")
bot.infinity_polling()
