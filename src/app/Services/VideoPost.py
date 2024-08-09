import time
import random
from .BaseService import BaseService
from ..Confs.TgApiConf import TgApiConf


class Video(BaseService):
    def save(self, message):
        response = self.requests.post(TgApiConf.https + "/CopyMessage",
                                      data={
                                          'chat_id': "@RandomniyVidoeChannel",
                                          'from_chat_id':  message.from_user.id,
                                          'message_id': message.message_id
                                      }
                                      ).json()
        messageId = response.get('result').get('message_id')
        self.postRepository.savePost(self.postRepository.video_type, messageId)

    def send(self, message):
        try:
            lastPostId = self.postRepository.getLastPostByType(self.postRepository.video_type)
            lastPostId = lastPostId[self.postRepository.field_entity_id]
            postId = int(random.randint(0, int(lastPostId)))
            curTime = time.gmtime(time.time() + (60 * 60 * 3))
            curTime = time.strftime("%H:%M:%S", curTime)
            print(str(message.from_user.username) + " (" + str(message.from_user.id) + ")-" + str(
                curTime) + "//ID видео-поста - " + str(postId) + ", последний ID - " + str(lastPostId))
            self.bot.copy_message(message.from_user.id, "@RandomniyVidoeChannel", postId, "")
        except():
            self.send(message)
