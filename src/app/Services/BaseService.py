import time
import random
import requests
from ..Repositories.PostRepository import PostRepository
from ..Confs.TgApiConf import TgApiConf


class BaseService:
    def __init__(self, bot):
        self.bot = bot
        self.postRepository = PostRepository()
        self.requests = requests
        self.time = time
        self.random = random
        self.TgApiConf = TgApiConf
