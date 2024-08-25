from ..Repositories.SubcsribersRepository import Subscribers
from telebot import types
from .BaseService import BaseService


class Payments(BaseService):

    price_one_month_subscribe = 50

    def sendInvoice(self, message):
        self.bot.send_invoice(
            message.chat.id,
            'Подписка на видео',
            'Дает возможность загружать и получать видео',
            message.from_user.id,
            '',
            'XTR',
            [
                types.LabeledPrice('XTR', self.price_one_month_subscribe)
            ],
            protect_content=True
        )

    def sendPreCheckOutQueryAnwer(self, pre_checkout_query):
        self.bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=True,
            error_message='Что то пошло не так, попробуйте еще раз'
        )

    def getTransactionsList(self):
        for transaction in self.bot.get_star_transactions().transactions:
            print(transaction)

    def successfulPayment(self, userId):
        subReps = Subscribers()
        subReps.addNewSubscriber(userId)
