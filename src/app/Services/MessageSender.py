from .BaseService import BaseService


class MessageSender(BaseService):
    def __init__(self, bot, logger):
        super().__init__(bot, logger)

    async def sendMessageToAllUsers(self, text: str):
        users = self.userRepository.getAllUsers()
        await self.logger.writeLog('Началась рассылка сообщения')
        for user in users:
            userId = user[self.userRepository.field_id]
            #await self.bot.send_message(
            #    chat_id=userId,
            #    text=text
            #)
            print(userId)
            await self.logger.writeLog(F'Сообщение отправлено юзеру {userId}')
        await self.logger.writeLog('Рассылка сообщения закончилась')