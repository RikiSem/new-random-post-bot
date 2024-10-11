import time
import random
import requests
from ..Confs.TgApiConf import TgApiConf
from telebot.async_telebot import AsyncTeleBot
from ..Repositories.PostRepository import PostRepository


class BaseService:
    def __init__(self, bot: AsyncTeleBot):
        self.bot = bot
        self.postRepository = PostRepository()
        self.requests = requests
        self.time = time
        self.random = random
        self.TgApiConf = TgApiConf
