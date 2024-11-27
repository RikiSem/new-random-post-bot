from app.Confs.TgApiConf import logChannel
from aiogram import Bot

class Logger():
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    async def writeLog(self, text):
        await self.bot.send_message(
            logChannel,
            text
        )