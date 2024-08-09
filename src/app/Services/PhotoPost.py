import time
import random
from .BaseService import BaseService
from ..Confs.TgApiConf import TgApiConf


class Photo(BaseService):
    def save(self, message):
        response = self.requests.post(TgApiConf.https + "/CopyMessage",
                                      data={
                                          'chat_id': '@RandomFotoChannel',
                                          'from_chat_id': message.from_user.id,
                                          'message_id': message.message_id
                                      }
                                      ).json()
        messageId = response.get('result').get('message_id')
        self.postRepository.savePost(self.postRepository.photo_type, messageId)

    def send(self, message):
        lastPostId = self.postRepository.getLastPostByType(self.postRepository.photo_type)
        lastPostId = lastPostId[self.postRepository.field_entity_id]

        firstPostId = self.postRepository.getFirstPostByType(self.postRepository.photo_type)
        firstPostId = firstPostId[self.postRepository.field_entity_id]

        postId = int(random.randint(firstPostId, int(lastPostId)))
        curTime = time.gmtime(time.time() + (60 * 60 * 3))
        curTime = time.strftime("%H:%M:%S", curTime)
        print(str(message.from_user.username) + " (" + str(message.from_user.id) + ")-" + str(
            curTime) + "//ID фото-поста - " + str(postId) + ", последний ID - " + str(lastPostId))
        try:
            self.bot.copy_message(message.from_user.id, "@RandomFotoChannel", postId, "")
        except():
            self.send(message)
