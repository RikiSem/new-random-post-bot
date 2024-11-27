import asyncio
from aiogram import Bot
from app.Repositories.BlackListRepository import BlackList
from aiogram.types import Message
from app.Confs.BotTexts import BotTexts
from typing import Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class CheckBlockList(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.blackList = BlackList()
        self.botText = BotTexts()
        self.userlang = 'ru'
        self.bot = bot

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, any]], Awaitable[any]],
            event: Message,
            data: Dict[str, any]
            ) -> any:
        if not await self.checkBlackList(event.from_user.id):
            await self.bot.send_message(event.from_user.id, self.botText.langs[self.userlang]['banned'])
        else:
            return await handler(event, data)
    
    async def checkBlackList(self, userId):
        result = True
        if self.blackList.getUser(userId=userId) is not None:
            result = False
        return result