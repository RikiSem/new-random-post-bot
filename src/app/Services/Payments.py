from .BaseService import BaseService
from aiogram.types import LabeledPrice
from ..Repositories.SubcsribersRepository import Subscribers


class Payments(BaseService):

    price_one_month_subscribe = 100

    async def sendInvoice(self, message):
        await self.bot.send_invoice(
            chat_id=message.chat.id,
            title='Подписка на премиум',
            description='Дает возможность использовать премиум функции бота(просмотр/загрузка видео и рулетка вайфу)',
            payload=str(message.from_user.id),
            currency='XTR',
            prices=[
                LabeledPrice(label='XTR', amount=self.price_one_month_subscribe)
            ],
            provider_token='',
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
