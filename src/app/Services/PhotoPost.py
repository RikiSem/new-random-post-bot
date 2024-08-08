import time
import random
from .BaseService import BaseService

class Photo(BaseService):
    def save(self):
        pass
    def send(self, message, posts, canSendFoto):
        try:
            userId = message.from_user.id
            postId = int(random.randint(12, int(posts)))
            curTime = time.time()
            curTime = time.gmtime(curTime + (60 * 60 * 3))
            curTime = time.strftime("%H:%M:%S", curTime)
            print(str(message.from_user.username) + " (" + str(message.from_user.id) + ")-" + str(
                curTime) + "//ID фото-поста - " + str(postId) + ", последний ID - " + str(posts))
            self.bot.copy_message(userId, "@RandomFotoChannel", postId, "")
            canSendFoto = False
        except:
            self.send(message, posts, canSendFoto)