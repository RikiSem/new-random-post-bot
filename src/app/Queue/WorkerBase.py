from aiogram.types import Message
from aiogram import Bot
from app.Services.Logger import Logger

class BaseWorker:
    def __init__(self, queue, bot: Bot, logger: Logger):
        self.queue = queue
        self.bot = bot
        self.logger = logger
