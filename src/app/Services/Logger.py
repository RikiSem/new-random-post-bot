from app.Confs.TgApiConf import logChannel
from telebot.async_telebot import AsyncTeleBot

class Logger():
    def __init__(self, bot: AsyncTeleBot) -> None:
        self.bot = bot


    async def writeLog(self, text):
        await self.bot.send_message(
            logChannel,
            text
        )