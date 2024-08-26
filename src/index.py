import telebot
import time
from datetime import datetime
from threading import Thread
from app.Confs.TgApiConf import TgApiConf
from app.Confs.TgConf import TgConf
from app.Services.VideoPost import Video
from app.Services.PhotoPost import Photo
from app.Repositories.SubcsribersRepository import Subscribers
from app.Repositories.BlackListRepository import BlackList
from app.Repositories.PostRepository import PostRepository
from app.Repositories.UserRepository import UserRepository
from app.Confs.BotButtons import BotButtons
from app.Confs.BotTexts import BotTexts
from app.Services.Payments import Payments
import app.Confs.Rules as rules

bot = telebot.TeleBot(TgApiConf.token, num_threads=10)
Photo = Photo(bot)
Video = Video(bot)
Payments = Payments(bot)
SubscribersRepository = Subscribers()
BlacklistRepository = BlackList()
PostRep = PostRepository()
userRep = UserRepository()
Https = TgApiConf.https
BotButtons = BotButtons()
BotTexts = BotTexts()

print("Start")

global canSendFoto, canSendVideo
canSendFoto = False
canSendVideo = False


def checkSubscriber(userId):
    result = False
    user = SubscribersRepository.getUser(userId=userId)
    if user is not None:
        subEndTime = user[SubscribersRepository.field_end]
        currentTime = datetime.utcfromtimestamp(time.time())
        if subEndTime > str(currentTime):
            result = True
    return result


def rememberUser(message):
    user = userRep.isUserExist(message.from_user.id)
    if not user:
        userRep.saveUser(message.from_user.id, message.from_user.username)


def checkBlackList(userId):
    result = True
    if BlacklistRepository.getUser(userId=userId) is not None:
        result = False
    return result


@bot.message_handler(commands=["start"])
def firstStart(message):
    global userLang
    rememberUser(message)
    userLang = 'en' if message.from_user.language_code not in ['ru', 'be', 'uk'] else 'ru'
    isAdmin = False
    if message.from_user.id in TgConf.admins:
        isAdmin = True
    currentMarkup = BotButtons.getAdminMarkup(userLang) if isAdmin else BotButtons.getMainMarkup(userLang)
    bot.send_message(
        message.from_user.id,
        f"{BotTexts.langs[userLang]['hello']}, {message.from_user.first_name}",
        reply_markup=currentMarkup
    )


@bot.message_handler(commands=["rules"])
def showRules(message):
    bot.send_message(
        message.from_user.id,
        'За нарушение правил может последовать блокировка'
    )
    bot.send_message(
        message.from_user.id,
        '\n'.join(rules.rules)
    )


@bot.message_handler(commands=["terms"])
def sendTerms(message):
    bot.send_message(
        message.from_user.id,
        'Используя данный бот, вы автоматически соглашаетесь в положениями пользовательского соглашения\n' +
        'Текст пользовательского соглашения доступен ниже\n' +
        'https://docs.google.com/document/d/1TNsyVFcinzruBtW_MRIB9seAoTHsUyLjKTUWjX02bRg/edit?usp=sharing'
    )


@bot.message_handler()
def handler(message):
    global canSendFoto, canSendVideo, userLang
    canSendFoto = False
    canSendVideo = False
    isAdmin = False
    rememberUser(message)
    userId = message.from_user.id
    userLang = 'en' if message.from_user.language_code not in ['ru', 'be', 'uk'] else 'ru'
    resultBlacklistCheck = checkBlackList(message.from_user.id)
    if message.from_user.id in TgConf.admins:
        isAdmin = True

    currentMarkup = BotButtons.getAdminMarkup(lang=userLang) if isAdmin else BotButtons.getMainMarkup(lang=userLang)

    if not resultBlacklistCheck:
        bot.send_message(userId, BotTexts.langs[userLang]['banned'])
    else:
        if message.text == BotButtons.langs[userLang]['randomFoto']:
            sendFotoThread = Thread(target=Photo.send(message))
            sendFotoThread.start()
        elif message.text == BotButtons.langs[userLang]['loadFoto']:
            canSendFoto = True
            canSendVideo = False
            bot.send_message(userId, BotTexts.langs[userLang]['sendFoto'])
        elif message.text in [BotButtons.langs[userLang]['randomVideo'], BotButtons.langs[userLang]['loadVideo']]:
            if checkSubscriber(str(message.from_user.id)) or userId in TgConf.admins:
                if message.text == BotButtons.langs[userLang]['randomVideo']:
                    sendVideoThread = Thread(target=Video.send(message))
                    sendVideoThread.start()
                else:
                    canSendVideo = True
                    canSendFoto = False
                    bot.send_message(userId, BotTexts.langs[userLang]['sendVideo'])
            else:
                bot.send_message(userId, BotTexts.langs[userLang]['subscriptionExpired'])
                bot.send_message(
                    userId,
                    BotTexts.langs[userLang]['pay_1'] + '\n' +
                    BotTexts.langs[userLang]['pay_2'] + '\n' +
                    BotTexts.langs[userLang]['pay_3'] + '\n' +
                    BotTexts.langs[userLang]['subСost'] +
                    ' - ' +
                    str(Payments.price_one_month_subscribe) +
                    ' ' +
                    BotTexts.langs[userLang]['stars'],
                    reply_markup=BotButtons.getSubMarkup(lang=userLang)
                )
        elif message.text == BotButtons.langs[userLang]['buy']:
            bot.send_message(userId, BotTexts.langs[userLang]['paymentMethod'],
                             reply_markup=BotButtons.getPayMarkup(lang=userLang))
        elif message.text == BotButtons.langs[userLang]['cancel']:
            bot.send_message(userId, BotTexts.langs[userLang]['good'] + ', ' + message.from_user.first_name,
                             reply_markup=currentMarkup)
        elif message.text == BotButtons.langs[userLang]['pay']:
            Payments.sendInvoice(message)
        elif message.text == BotButtons.langs[userLang]['admin_transactions']:
            if not userId in TgConf.admins:
                bot.send_message(userId, BotTexts.langs[userLang]['howInAdmin'], reply_markup=currentMarkup)
            else:
                Payments.getTransactionsList()
                bot.send_message(userId, BotTexts.langs[userLang]['logs'], reply_markup=currentMarkup)


@bot.message_handler(content_types=['photo'])
def saveFoto(message):
    global canSendFoto
    if canSendFoto:
        Photo.save(message)
        print(str(message.from_user.username) + "//Состояние в saveFoto - " + str(canSendFoto))
        bot.send_message(message.from_user.id, BotTexts.langs[userLang]['photoAdded'])
        canSendFoto = False
    elif not canSendFoto:
        bot.send_message(message.from_user.id,
                         f"{BotTexts.langs[userLang]['first_press_the_button']} '{BotButtons.langs[userLang]['loadFoto']}'")


@bot.message_handler(content_types=['video'])
def saveVideo(message):
    global canSendVideo
    if canSendVideo:
        Video.save(message)
        print(str(message.from_user.username) + "//Состояние в saveVideo - " + str(canSendVideo))
        bot.send_message(message.from_user.id, BotTexts.langs[userLang]['videoAdded'])
        canSendVideo = False
    elif not canSendVideo:
        bot.send_message(message.from_user.id,
                         f"{BotTexts.langs[userLang]['first_press_the_button']} '{BotButtons.langs[userLang]['loadVideo']}'")


@bot.pre_checkout_query_handler(func=lambda query: True)
def preCheckoutQuery(pre_checkout_query):
    print(f'preCheckoutQuery оплаты подписки пользователем {pre_checkout_query.from_user.id}')
    Payments.sendPreCheckOutQueryAnwer(pre_checkout_query)


@bot.message_handler(content_types=['successful_payment'])
def successfulPayment(message):
    userId = message.from_user.id
    try:
        Payments.successfulPayment(userId)
        bot.send_message(
            userId,
            f"{BotTexts.langs[userLang]['thank_you_for_purchasing_a_subscription']}!",
            reply_markup=BotButtons.getMainMarkup(lang=userLang)
        )
        print(f'Пользователь {userId} оформил подписку на 30 дней')
    except():
        print(f'Неоформилась подписка у пользователя {userId}')


print("Started")
bot.infinity_polling()
