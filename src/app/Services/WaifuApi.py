import random
import requests
from .BaseService import BaseService, AsyncTeleBot

class WaifuApi(BaseService):

    getTagsUrl = 'https://api.waifu.im/tags'
    apiUrl = 'https://api.waifu.im/search'

    nsfwTagsKey = 'nsfw'
    versatileTagsKey = 'versatile'

    def __init__(self, bot: AsyncTeleBot):
        super().__init__(bot)
        self.nsfwTags = self.getTags(self.nsfwTagsKey)
        self.versatile = self.getTags(self.versatileTagsKey)

    def getTags(self, type):
        match type:
            case self.nsfwTagsKey:
                result = requests.get(self.getTagsUrl).json()[type]
            case self.versatileTagsKey:
                result = requests.get(self.getTagsUrl).json()[type]
        return result

    async def getRandomWaifu(self, chatId: int):
        match random.randint(0, 1):
            case 0:
                result = self.getNsfwWaifu()
            case 1:
                result = self.getVersatileWaifu()
        try:
            await self.bot.send_photo(chatId, result)
        except:
            await self.getRandomWaifu(chatId)

    def getNsfwWaifu(self):
        try:
            params = {
                'included_tags': [random.choice(self.nsfwTags)],
            }
            return self.sendRequest(params)
        except:
            self.getNsfwWaifu()

    def getVersatileWaifu(self):
        try:
            params = {
                'included_tags': [random.choice(self.versatile)],
            }
            return self.sendRequest(params)
        except:
            self.getVersatileWaifu()

    def sendRequest(self, params):
        response = requests.get(self.apiUrl, params=params).json()['images'][0]['url']
        return response