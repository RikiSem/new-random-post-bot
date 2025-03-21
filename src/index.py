import time
import random
import logging
import asyncio
from datetime import datetime
import app.Confs.Rules as rules
from app.Confs.TgConf import TgConf
from aiogram.types import ContentType
from app.Services.Logger import Logger
from app.Confs.BotTexts import BotTexts
from app.Services.VideoPost import Video
from app.Services.PhotoPost import Photo
from app.Confs.TgApiConf import TgApiConf
from app.Services.Payments import Payments
from app.Services.WaifuApi import WaifuApi
from app.Confs.BotButtons import BotButtons
from aiogram.filters.command import Command
from app.Confs.premiumItems import premiumItems
from app.Services.MessageSender import MessageSender
from aiogram.handlers import PreCheckoutQueryHandler
from aiogram import Bot, Dispatcher, types, F, Router
from app.Middleware.checkBlockList import CheckBlockList
from app.Queue.SendMessageWorker import SendMessageWorker
from app.Repositories.BlackListRepository import BlackList
from app.Repositories.PostRepository import PostRepository
from app.Repositories.UserRepository import UserRepository
from app.Repositories.SubcsribersRepository import Subscribers
from app.Middleware.checkSubscription import CheckSubscription

print("Loading....")
bot = Bot(TgApiConf.token)
dp = Dispatcher()
dp.message.middleware(CheckBlockList(bot))
dp.message.middleware(CheckSubscription(bot))
router = Router()
logging.basicConfig(level=logging.INFO)
logger = Logger(bot)
photo = Photo(bot, logger)
video = Video(bot, logger)
payments = Payments(bot, logger)
waifuApi = WaifuApi(bot, logger)
messageSender = MessageSender(bot, logger)
SubscribersRepository = Subscribers()
BlacklistRepository = BlackList()
PostRep = PostRepository()
userRep = UserRepository()
Https = TgApiConf.https
botButtons = BotButtons()
botTexts = BotTexts()

queue = asyncio.Queue()
sendMessageWorker = SendMessageWorker(queue, bot, logger)

global canSendFoto, canSendVideo, canSendMessage
canSendMessage = False
canSendFoto = False
canSendVideo = False
canBlockUser = False


async def checkSubscriber(userId: int):
    result = False
    user = SubscribersRepository.getUser(userId=userId)
    if user is not None:
        subEndTime = user[SubscribersRepository.field_end]
        currentTime = datetime.utcfromtimestamp(time.time())
        if subEndTime > str(currentTime):
            result = True
    return result


async def rememberUser(message: types.Message):
    user = userRep.isUserExist(message.from_user.id)
    if not user:
        userRep.saveUser(message.from_user.id, message.from_user.username)


async def checkBlackList(userId: int):
    result = True
    if BlacklistRepository.getUser(userId=userId) is not None:
        result = False
    return result

async def sendAds(userId: int):
    await bot.send_message(
        chat_id=userId,
        text='''
        Оформи подписку и получишь доступ к сотням видео и не только\n
        Жми -> /buy\n
        Так же, ты можешь стать участником партнерской программы и получать до 50 процентов от трат тех, кто пройдет по твоей ссылке и купит подписку\n
        Для этого нажми на название бота и выбери 'Партнерская программа'
        '''
    )

async def subscriptionExpired(userId: int):
    await bot.send_message(userId, botTexts.langs['ru']['subscriptionExpired'])
    await bot.send_message(
        userId,
        botTexts.langs['ru']['pay_1'] + '\n' +
        botTexts.langs['ru']['pay_2'] + '\n' +
        botTexts.langs['ru']['pay_3'] + '\n' +
        botTexts.langs['ru']['subСost'] +
        ' - ' +
        str(payments.price_one_month_subscribe) +
        ' ' +
        botTexts.langs['ru']['stars'],
        reply_markup=botButtons.getSubMarkup(lang='ru')
    )


@dp.message(Command('start'))
async def firstStart(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    await rememberUser(message)
    currentMarkup = botButtons.getMainMarkup(lang=userLang)
    if (isSubscriber):
        currentMarkup = botButtons.getPremiumMarkup(lang=userLang)
    if (isAdmin):
        currentMarkup = botButtons.getAdminMarkup(lang=userLang)
    await bot.send_message(
        userId,
        f"{botTexts.langs[userLang]['hello']}, {message.from_user.first_name}",
        reply_markup=currentMarkup
    )


@dp.message(Command('rules'))
async def showRules(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    await bot.send_message(
        userId,
        'За нарушение правил может последовать блокировка'
    )
    await bot.send_message(
        userId,
        '\n'.join(rules.rules)
    )


@dp.message(Command('terms'))
async def sendTerms(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    await bot.send_message(
        userId,
        'Используя данный бот, вы автоматически соглашаетесь в положениями пользовательского соглашения\n' +
        'Текст пользовательского соглашения доступен ниже\n' +
        'https://docs.google.com/document/d/1TNsyVFcinzruBtW_MRIB9seAoTHsUyLjKTUWjX02bRg/edit?usp=sharing'
    )


@dp.message(F.text == botButtons.langs['ru']['randomFoto'])
async def randomFoto(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    if (showAds and not isAdmin and not isSubscriber):
        await sendAds(userId)
    await photo.send(message)


@dp.message(F.text == botButtons.langs['ru']['loadFoto'])
async def loadFoto(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    global canSendFoto, canSendVideo
    canSendFoto = True
    canSendVideo = False
    if (showAds and not isAdmin and not isSubscriber):
        await sendAds(userId)
    await bot.send_message(userId, botTexts.langs[userLang]['sendFoto'])

@dp.message(F.text == botButtons.langs['ru']['adminSendMessage'])
async def adminSendMessage(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    global canSendMessage
    if (isAdmin):
        await bot.send_message(
            chat_id=userId,
            text='Напиши сообщение'
        )
        canSendMessage = True

@dp.message(F.text == botButtons.langs['ru']['blockUser'])
async def setBlockUserId(message: types.Message, isSubscriber, isAdmin, userLang, userId):
        global canBlockUser
        await bot.send_message(
            chat_id=userId,
            text='Введи id пользователя'
        )
        canBlockUser = True

"""@dp.message(F.text)
async def sendMessageToUsers(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    global canSendMessage
    if (isAdmin and canSendMessage and (message.text not in botButtons.langs[userLang].values())):
        await messageSender.sendMessageToAllUsers(message.text)
        canSendMessage = False
        await bot.send_message(
            chat_id=userId,
            text='Сообщение разослано'
        )
"""

@dp.message(Command('buy'))
@dp.message(F.text == botButtons.langs['ru']['buyPremium'])
async def buyPremium(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    if (isAdmin or isSubscriber):
        await bot.send_message(
            chat_id=userId,
            text='У вас уже оформлена месячная подписка',
            reply_markup=botButtons.getPremiumMarkup(lang=userLang)
        )
    else:
        await bot.send_message(
            userId,
            botTexts.langs[userLang]['pay_1'] + '\n' +
            botTexts.langs[userLang]['pay_2'] + '\n' +
            botTexts.langs[userLang]['pay_3'] + '\n' +
            botTexts.langs[userLang]['subСost'] +
            ' - ' +
            str(payments.price_one_month_subscribe) +
            ' ' +
            botTexts.langs[userLang]['stars'],
            reply_markup=botButtons.getSubMarkup(lang=userLang)
        )


@dp.message(F.text == botButtons.langs['ru']['randomVideo'])
async def randomVideo(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    if (isAdmin or isSubscriber):
        await video.send(message)
    else:
        await subscriptionExpired(userId)


@dp.message(F.text == botButtons.langs['ru']['loadVideo'])
async def loadVideo(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    global canSendFoto, canSendVideo
    if (isAdmin or isSubscriber):
        canSendVideo = True
        canSendFoto = False
        await bot.send_message(userId, botTexts.langs[userLang]['sendVideo'])
    else:
        await subscriptionExpired(userId)


@dp.message(F.text == botButtons.langs['ru']['waifu'])
async def waifu(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    if (isAdmin or isSubscriber):
        await waifuApi.getRandomWaifu(message.chat.id)
    else:
        await subscriptionExpired(userId)


@dp.message(F.text == botButtons.langs['ru']['buy'])
async def buy(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    await bot.send_message(userId, botTexts.langs[userLang]['paymentMethod'],
                             reply_markup=botButtons.getPayMarkup(lang=userLang))



@dp.message(F.text == botButtons.langs['ru']['cancel'])
async def cancel(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    await bot.send_message(userId, botTexts.langs[userLang]['good'] + ', ' + message.from_user.first_name,
                             reply_markup=botButtons.getMainMarkup(lang=userLang))


@dp.message(F.text == botButtons.langs['ru']['pay'])
async def pay(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    await payments.sendInvoice(message)


@dp.message(F.content_type == ContentType.PHOTO)
async def saveFoto(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    global canSendFoto
    if canSendFoto:
        asyncio.gather(
            photo.save(message),
            logger.writeLog(f'Юзер @{str(message.from_user.username)} добавил фото'),
            bot.send_message(message.from_user.id, botTexts.langs[userLang]['photoAdded'])
            )
        canSendFoto = False
    elif not canSendFoto:
        await bot.send_message(message.from_user.id,
                         f"{botTexts.langs[userLang]['first_press_the_button']} '{botButtons.langs[userLang]['loadFoto']}'")


@dp.message(F.content_type == ContentType.VIDEO)
async def saveVideo(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    global canSendVideo
    if canSendVideo:
        asyncio.gather(
            video.save(message),
            logger.writeLog(f'Юзер @{str(message.from_user.username)} добавил видео'),
            bot.send_message(message.from_user.id, botTexts.langs[userLang]['videoAdded'])
        )
        canSendVideo = False
    elif not canSendVideo:
        await bot.send_message(message.from_user.id,
                         f"{botTexts.langs[userLang]['first_press_the_button']} '{botButtons.langs[userLang]['loadVideo']}'")
    elif not canSendVideo and not isSubscriber:
        await bot.send_message(message.from_user.id,
                    f'Чтобы загружать свои видео необходимо купить подписку')


@dp.pre_checkout_query()
async def preCheckoutQuery(pre_checkout_query: types.PreCheckoutQuery):
    await logger.writeLog(f'preCheckoutQuery оплаты подписки пользователем {pre_checkout_query.from_user.id}')
    print(f'preCheckoutQuery оплаты подписки пользователем {pre_checkout_query.from_user.id}')
    await payments.sendPreCheckOutQueryAnwer(pre_checkout_query)


@dp.message(F.successful_payment)
async def successfulPayment(message: types.Message, isSubscriber, isAdmin, userLang, userId, showAds):
    userId = message.from_user.id
    try:
        payments.successfulPayment(userId)
        await bot.send_message(
            userId,
            f"{botTexts.langs[userLang]['thank_you_for_purchasing_a_subscription']}!",
            reply_markup=botButtons.getMainMarkup(lang=userLang)
        )
        logger.writeLog(f'Пользователь {userId} оформил подписку на 30 дней')
        print(f'Пользователь {userId} оформил подписку на 30 дней')
    except():
        f'Неоформилась подписка у пользователя {userId}'
        print(f'Неоформилась подписка у пользователя {userId}')

@dp.message()
async def blockUser(message: types.Message, isSubscriber, isAdmin, userLang, userId):
    global canBlockUser
    if (canBlockUser and isAdmin):
        BlacklistRepository.blockUser(int(message.text))
        await bot.send_message(
            chat_id=userId,
            text=f'Пользователь {message.text} заблокирован',
        )
        canBlockUser = False
    else:
        await bot.send_message(
            chat_id=userId,
            text='Что?'
        )

async def main():
    asyncio.gather(
        await dp.start_polling(bot),
        await sendMessageWorker.work(queue)
    )



print("Started")
if __name__ == '__main__':
    asyncio.run(main())
