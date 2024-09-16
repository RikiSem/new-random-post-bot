
import time
import asyncio
from threading import Thread
from datetime import datetime
import app.Confs.Rules as rules
from app.Confs.TgConf import TgConf
from app.Confs.BotTexts import BotTexts
from app.Services.VideoPost import Video
from app.Services.PhotoPost import Photo
from app.Confs.TgApiConf import TgApiConf
from app.Services.Payments import Payments
from app.Confs.BotButtons import BotButtons
from telebot.async_telebot import AsyncTeleBot
from app.Repositories.BlackListRepository import BlackList
from app.Repositories.PostRepository import PostRepository
from app.Repositories.UserRepository import UserRepository
from app.Repositories.SubcsribersRepository import Subscribers

bot = AsyncTeleBot(TgApiConf.token)
photo = Photo(bot)
video = Video(bot)
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


async def checkSubscriber(userId):
    result = False
    user = SubscribersRepository.getUser(userId=userId)
    if user is not None:
        subEndTime = user[SubscribersRepository.field_end]
        currentTime = datetime.utcfromtimestamp(time.time())
        if subEndTime > str(currentTime):
            result = True
    return result


async def rememberUser(message):
    user = userRep.isUserExist(message.from_user.id)
    if not user:
        userRep.saveUser(message.from_user.id, message.from_user.username)


async def checkBlackList(userId):
    result = True
    if BlacklistRepository.getUser(userId=userId) is not None:
        result = False
    return result


@bot.message_handler(commands=["start"])
async def firstStart(message):
    global userLang
    await rememberUser(message)
    userLang = 'en' if message.from_user.language_code not in ['ru', 'be', 'uk'] else 'ru'
    isAdmin = False
    if message.from_user.id in TgConf.admins:
        isAdmin = True
    currentMarkup = BotButtons.getAdminMarkup(userLang) if isAdmin else BotButtons.getMainMarkup(userLang)
    await bot.send_message(
        message.from_user.id,
        f"{BotTexts.langs[userLang]['hello']}, {message.from_user.first_name}",
        reply_markup=currentMarkup
    )


@bot.message_handler(commands=["rules"])
async def showRules(message):
    await bot.send_message(
        message.from_user.id,
        'За нарушение правил может последовать блокировка'
    )
    await bot.send_message(
        message.from_user.id,
        '\n'.join(rules.rules)
    )


@bot.message_handler(commands=["terms"])
async def sendTerms(message):
    await bot.send_message(
        message.from_user.id,
        'Используя данный бот, вы автоматически соглашаетесь в положениями пользовательского соглашения\n' +
        'Текст пользовательского соглашения доступен ниже\n' +
        'https://docs.google.com/document/d/1TNsyVFcinzruBtW_MRIB9seAoTHsUyLjKTUWjX02bRg/edit?usp=sharing'
    )


@bot.message_handler()
async def handler(message):
    global canSendFoto, canSendVideo, userLang
    canSendFoto = False
    canSendVideo = False
    isAdmin = False
    await rememberUser(message)
    userId = message.from_user.id
    userLang = 'en' if message.from_user.language_code not in ['ru', 'be', 'uk'] else 'ru'
    resultBlacklistCheck = await checkBlackList(message.from_user.id)
    if message.from_user.id in TgConf.admins:
        isAdmin = True

    currentMarkup = BotButtons.getAdminMarkup(lang=userLang) if isAdmin else BotButtons.getMainMarkup(lang=userLang)

    if not resultBlacklistCheck:
        await bot.send_message(userId, BotTexts.langs[userLang]['banned'])
    else:
        if message.text == BotButtons.langs[userLang]['randomFoto']:
            await photo.send(message)
        elif message.text == BotButtons.langs[userLang]['loadFoto']:
            canSendFoto = True
            canSendVideo = False
            await bot.send_message(userId, BotTexts.langs[userLang]['sendFoto'])
        elif message.text in [BotButtons.langs[userLang]['randomVideo'], BotButtons.langs[userLang]['loadVideo']]:
            if checkSubscriber(str(message.from_user.id)) or userId in TgConf.admins:
                if message.text == BotButtons.langs[userLang]['randomVideo']:
                    await video.send(message)
                else:
                    canSendVideo = True
                    canSendFoto = False
                    await bot.send_message(userId, BotTexts.langs[userLang]['sendVideo'])
            else:
                await bot.send_message(userId, BotTexts.langs[userLang]['subscriptionExpired'])
                await bot.send_message(
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
            await bot.send_message(userId, BotTexts.langs[userLang]['paymentMethod'],
                             reply_markup=BotButtons.getPayMarkup(lang=userLang))
        elif message.text == BotButtons.langs[userLang]['cancel']:
            await bot.send_message(userId, BotTexts.langs[userLang]['good'] + ', ' + message.from_user.first_name,
                             reply_markup=currentMarkup)
        elif message.text == BotButtons.langs[userLang]['pay']:
            await Payments.sendInvoice(message)
        elif message.text == BotButtons.langs[userLang]['admin_transactions']:
            if not userId in TgConf.admins:
                await bot.send_message(userId, BotTexts.langs[userLang]['howInAdmin'], reply_markup=currentMarkup)
            else:
                await Payments.getTransactionsList()
                await bot.send_message(userId, BotTexts.langs[userLang]['logs'], reply_markup=currentMarkup)


@bot.message_handler(content_types=['photo'])
async def saveFoto(message):
    global canSendFoto
    if canSendFoto:
        photo.save(message)
        print(str(message.from_user.username) + "//Состояние в saveFoto - " + str(canSendFoto))
        await bot.send_message(message.from_user.id, BotTexts.langs[userLang]['photoAdded'])
        canSendFoto = False
    elif not canSendFoto:
        await bot.send_message(message.from_user.id,
                         f"{BotTexts.langs[userLang]['first_press_the_button']} '{BotButtons.langs[userLang]['loadFoto']}'")


@bot.message_handler(content_types=['video'])
async def saveVideo(message):
    global canSendVideo
    if canSendVideo:
        video.save(message)
        print(str(message.from_user.username) + "//Состояние в saveVideo - " + str(canSendVideo))
        await bot.send_message(message.from_user.id, BotTexts.langs[userLang]['videoAdded'])
        canSendVideo = False
    elif not canSendVideo:
        await bot.send_message(message.from_user.id,
                         f"{BotTexts.langs[userLang]['first_press_the_button']} '{BotButtons.langs[userLang]['loadVideo']}'")


@bot.pre_checkout_query_handler(func=lambda query: True)
def preCheckoutQuery(pre_checkout_query):
    print(f'preCheckoutQuery оплаты подписки пользователем {pre_checkout_query.from_user.id}')
    Payments.sendPreCheckOutQueryAnwer(pre_checkout_query)


@bot.message_handler(content_types=['successful_payment'])
async def successfulPayment(message):
    userId = message.from_user.id
    try:
        Payments.successfulPayment(userId)
        await bot.send_message(
            userId,
            f"{BotTexts.langs[userLang]['thank_you_for_purchasing_a_subscription']}!",
            reply_markup=BotButtons.getMainMarkup(lang=userLang)
        )
        print(f'Пользователь {userId} оформил подписку на 30 дней')
    except():
        print(f'Неоформилась подписка у пользователя {userId}')


print("Started")
asyncio.run(bot.infinity_polling())
