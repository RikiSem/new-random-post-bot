from .BaseService import BaseService


class MessageSender(BaseService):
    async def sendMessageToAllUsers(self, text: str):
        users = self.userRepository.getAllUsers()
        await self.logger.writeLog('Началась рассылка сообщения')
        for user in users:
            userId = user[self.userRepository.field_id]
            await self.bot.send_message(
                chat_id=userId,
                text=text
            )
        await self.logger.writeLog('Рассылка сообщения закончилась')