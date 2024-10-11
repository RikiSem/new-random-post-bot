
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
from app.Services.WaifuApi import WaifuApi
from app.Confs.BotButtons import BotButtons
from app.Confs.premiumItems import premiumItems
from telebot.async_telebot import AsyncTeleBot, types
from app.Repositories.BlackListRepository import BlackList
from app.Repositories.PostRepository import PostRepository
from app.Repositories.UserRepository import UserRepository
from app.Repositories.SubcsribersRepository import Subscribers

print("Loading....")
bot = AsyncTeleBot(TgApiConf.token)
photo = Photo(bot)
video = Video(bot)
Payments = Payments(bot)
waifuApi = WaifuApi(bot)
SubscribersRepository = Subscribers()
BlacklistRepository = BlackList()
PostRep = PostRepository()
userRep = UserRepository()
Https = TgApiConf.https
botButtons = BotButtons()
botTexts = BotTexts()


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
    isAdmin = True if message.from_user.id in TgConf.admins else False
    premiumUser = await checkSubscriber(str(message.from_user.id))
    currentMarkup = botButtons.getMainMarkup(lang=userLang)
    if (isAdmin or premiumUser):
        currentMarkup = botButtons.getPremiumMarkup(lang=userLang)
    await bot.send_message(
        message.from_user.id,
        f"{botTexts.langs[userLang]['hello']}, {message.from_user.first_name}",
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
async def handler(message: types.Message):
    global canSendFoto, canSendVideo, userLang
    canSendFoto = False
    canSendVideo = False
    isAdmin = True if message.from_user.id in TgConf.admins else False
    premiumUser = await checkSubscriber(str(message.from_user.id))
    await rememberUser(message)
    userId = message.from_user.id
    userLang = 'ru' #'en' if message.from_user.language_code not in ['ru', 'be', 'uk'] else 'ru'
    resultBlacklistCheck = await checkBlackList(message.from_user.id)
    if message.from_user.id in TgConf.admins:
        isAdmin = True

    currentMarkup = botButtons.getMainMarkup(lang=userLang)
    if (isAdmin or premiumUser):
        currentMarkup = botButtons.getPremiumMarkup(lang=userLang)

    if not resultBlacklistCheck:
        await bot.send_message(userId, botTexts.langs[userLang]['banned'])
    else:
        if message.text == botButtons.langs[userLang]['randomFoto']:
            await photo.send(message)
        elif message.text == botButtons.langs[userLang]['loadFoto']:
            canSendFoto = True
            canSendVideo = False
            await bot.send_message(userId, botTexts.langs[userLang]['sendFoto'])
        elif message.text == botButtons.langs[userLang]['buyPremium']:
            await bot.send_message(
                userId,
                botTexts.langs[userLang]['pay_1'] + '\n' +
                botTexts.langs[userLang]['pay_2'] + '\n' +
                botTexts.langs[userLang]['pay_3'] + '\n' +
                botTexts.langs[userLang]['subСost'] +
                ' - ' +
                str(Payments.price_one_month_subscribe) +
                ' ' +
                botTexts.langs[userLang]['stars'],
                reply_markup=botButtons.getSubMarkup(lang=userLang)
            )
        elif message.text in premiumItems:
            if premiumUser or isAdmin:
                if message.text == botButtons.langs[userLang]['randomVideo']:
                    await video.send(message)
                elif message.text == botButtons.langs[userLang]['loadVideo']:
                    canSendVideo = True
                    canSendFoto = False
                    await bot.send_message(userId, botTexts.langs[userLang]['sendVideo'])
                elif message.text == botButtons.langs[userLang]['waifu']:
                    await waifuApi.getRandomWaifu(message.chat.id)
            else:
                await bot.send_message(userId, botTexts.langs[userLang]['subscriptionExpired'])
                await bot.send_message(
                    userId,
                    botTexts.langs[userLang]['pay_1'] + '\n' +
                    botTexts.langs[userLang]['pay_2'] + '\n' +
                    botTexts.langs[userLang]['pay_3'] + '\n' +
                    botTexts.langs[userLang]['subСost'] +
                    ' - ' +
                    str(Payments.price_one_month_subscribe) +
                    ' ' +
                    botTexts.langs[userLang]['stars'],
                    reply_markup=botButtons.getSubMarkup(lang=userLang)
                )
        elif message.text == botButtons.langs[userLang]['buy']:
            await bot.send_message(userId, botTexts.langs[userLang]['paymentMethod'],
                             reply_markup=botButtons.getPayMarkup(lang=userLang))
        elif message.text == botButtons.langs[userLang]['cancel']:
            await bot.send_message(userId, botTexts.langs[userLang]['good'] + ', ' + message.from_user.first_name,
                             reply_markup=currentMarkup)
        elif message.text == botButtons.langs[userLang]['pay']:
            await Payments.sendInvoice(message)
        elif message.text == botButtons.langs[userLang]['admin_transactions']:
            if not userId in TgConf.admins:
                await bot.send_message(userId, botTexts.langs[userLang]['howInAdmin'], reply_markup=currentMarkup)
            else:
                await Payments.getTransactionsList()
                await bot.send_message(userId, botTexts.langs[userLang]['logs'], reply_markup=currentMarkup)


@bot.message_handler(content_types=['photo'])
async def saveFoto(message):
    global canSendFoto
    if canSendFoto:
        photo.save(message)
        print(str(message.from_user.username) + "//Состояние в saveFoto - " + str(canSendFoto))
        await bot.send_message(message.from_user.id, botTexts.langs[userLang]['photoAdded'])
        canSendFoto = False
    elif not canSendFoto:
        await bot.send_message(message.from_user.id,
                         f"{botTexts.langs[userLang]['first_press_the_button']} '{botButtons.langs[userLang]['loadFoto']}'")


@bot.message_handler(content_types=['video'])
async def saveVideo(message):
    global canSendVideo
    if canSendVideo:
        video.save(message)
        print(str(message.from_user.username) + "//Состояние в saveVideo - " + str(canSendVideo))
        await bot.send_message(message.from_user.id, botTexts.langs[userLang]['videoAdded'])
        canSendVideo = False
    elif not canSendVideo:
        await bot.send_message(message.from_user.id,
                         f"{botTexts.langs[userLang]['first_press_the_button']} '{botButtons.langs[userLang]['loadVideo']}'")


@bot.pre_checkout_query_handler(func=lambda query: True)
async def preCheckoutQuery(pre_checkout_query):
    print(f'preCheckoutQuery оплаты подписки пользователем {pre_checkout_query.from_user.id}')
    await Payments.sendPreCheckOutQueryAnwer(pre_checkout_query)


@bot.message_handler(content_types=['successful_payment'])
async def successfulPayment(message):
    userId = message.from_user.id
    try:
        Payments.successfulPayment(userId)
        await bot.send_message(
            userId,
            f"{botTexts.langs[userLang]['thank_you_for_purchasing_a_subscription']}!",
            reply_markup=botButtons.getMainMarkup(lang=userLang)
        )
        print(f'Пользователь {userId} оформил подписку на 30 дней')
    except():
        print(f'Неоформилась подписка у пользователя {userId}')


print("Started")
asyncio.run(bot.infinity_polling())
