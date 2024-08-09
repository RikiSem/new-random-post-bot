import requests
from ..Repositories.PostRepository import PostRepository


class BaseService:
    def __init__(self, bot):
        self.bot = bot
        self.postRepository = PostRepository()
        self.requests = requests
