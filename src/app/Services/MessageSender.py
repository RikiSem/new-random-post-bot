import time
from .BaseService import BaseService


class MessageSender(BaseService):
    def __init__(self, bot, logger):
        super().__init__(bot, logger)

    async def sendMessageToAllUsers(self, text: str):
        users = self.userRepository.getAllUsers()
        await self.logger.writeLog('Началась рассылка сообщения')
        for user in users:
            userId = user[self.userRepository.field_user_id]
            try:
                await self.bot.send_message(
                    chat_id=userId,
                    text=text
                )
                await self.logger.writeLog(F'Сообщение отправлено юзеру {userId}')
            except():
                await self.logger.writeLog(F'Юзер {userId} заблокировал бота')
            time.sleep(1)
        await self.logger.writeLog('Рассылка сообщения закончилась')