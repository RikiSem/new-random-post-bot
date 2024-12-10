import time
import random
import requests
from app.Services.Logger import Logger
from ..Confs.TgApiConf import TgApiConf
from aiogram import Bot
from ..Repositories.PostRepository import PostRepository
from ..Repositories.UserRepository import UserRepository


class BaseService:
    def __init__(self, bot: Bot, logger: Logger):
        self.bot = bot
        self.postRepository = PostRepository()
        self.userRepository = UserRepository()
        self.requests = requests
        self.time = time
        self.random = random
        self.TgApiConf = TgApiConf
        self.logger = logger
