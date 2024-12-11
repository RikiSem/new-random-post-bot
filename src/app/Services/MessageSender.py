from .BaseService import BaseService, types


class MessageSender(BaseService):
    def __init__(self, bot, logger):
        super().__init__(bot, logger)

    async def sendMessageToAllUsers(self, text: str):
        users = self.userRepository.getAllUsers()
        await self.logger.writeLog('Началась рассылка сообщения')
        for user in users:
            userId = user[self.userRepository.field_user_id]
            if isinstance(
                await self.bot.send_message(
                    chat_id=userId,
                    text=text
                ),
                types.Message
                ):
                await self.logger.writeLog(F'Сообщение отправлено юзеру {userId}')
            else:
                await self.logger.writeLog(F'Юзеру {userId} сообщение не отправлено')
            self.time.sleep(5)
        await self.logger.writeLog('Рассылка сообщения закончилась')