from telebot import types
from .BaseService import BaseService
from ..Repositories.SubcsribersRepository import Subscribers


class Payments(BaseService):

    price_one_month_subscribe = 100

    async def sendInvoice(self, message):
        await self.bot.send_invoice(
            message.chat.id,
            'Подписка на премиум',
            'Дает возможность использовать премиум функции бота(просмотр/загрузка видео и рулетка вайфу)',
            message.from_user.id,
            '',
            'XTR',
            [
                types.LabeledPrice('XTR', self.price_one_month_subscribe)
            ],
            protect_content=True
        )

    async def sendPreCheckOutQueryAnwer(self, pre_checkout_query):
        await self.bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=True,
            error_message='Что то пошло не так, попробуйте еще раз'
        )

    async def getTransactionsList(self):
        for transaction in self.bot.get_star_transactions().transactions:
            print(transaction)

    def successfulPayment(self, userId):
        subReps = Subscribers()
        subReps.addNewSubscriber(userId)
