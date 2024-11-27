import time
import asyncio
from app.Confs.TgConf import TgConf
from aiogram import Bot
from datetime import datetime
from app.Repositories.SubcsribersRepository import Subscribers
from aiogram.types import Message
from app.Confs.BotTexts import BotTexts
from typing import Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

class CheckSubscription(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.subscribers = Subscribers()
        self.botText = BotTexts()
        self.userlang = 'ru'
        self.bot = bot

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, any]], Awaitable[any]],
            event: Message,
            data: Dict[str, any]
            ) -> any:
        data['isSubscriber'] = await self.checkSubscriber(event.from_user.id)
        data['isAdmin'] = True if event.from_user.id in TgConf.admins else False
        data['userLang'] = 'ru'
        data['userId'] = event.from_user.id
        data['markup'] = None
        return await handler(event, data)

    async def checkSubscriber(self, userId: int):
        result = False
        user = self.subscribers.getUser(userId=userId)
        if user is not None:
            subEndTime = user[self.subscribers.field_end]
            currentTime = datetime.utcfromtimestamp(time.time())
            if subEndTime > str(currentTime):
                result = True
        return result