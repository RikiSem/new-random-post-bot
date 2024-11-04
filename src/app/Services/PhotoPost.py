from .BaseService import BaseService


class Photo(BaseService):
    def save(self, message):
        response = self.requests.post(self.TgApiConf.https + "/CopyMessage",
                                      data={
                                          'chat_id': '@RandomFotoChannel',
                                          'from_chat_id': message.from_user.id,
                                          'message_id': message.message_id,
                                          'caption': message.from_user.id
                                      }
                                      ).json()
        messageId = response.get('result').get('message_id')
        self.postRepository.savePost(self.postRepository.photo_type, messageId)

    async def send(self, message):
        lastPostId = self.postRepository.getLastPostByType(self.postRepository.photo_type)
        lastPostId = lastPostId[self.postRepository.field_entity_id]

        firstPostId = self.postRepository.getFirstPostByType(self.postRepository.photo_type)
        firstPostId = firstPostId[self.postRepository.field_entity_id]

        postId = int(self.random.randint(firstPostId, int(lastPostId)))
        curTime = self.time.gmtime(self.time.time() + (60 * 60 * 3))
        curTime = self.time.strftime("%H:%M:%S", curTime)
        await self.logger.writeLog(f'@{str(message.from_user.username)} ({str(message.from_user.id)})-{str(
            curTime)}//ID фото-поста - {str(postId)}, последний ID - {str(lastPostId)}')
        print(f'{str(message.from_user.username)} ({str(message.from_user.id)})-{str(
            curTime)}//ID фото-поста - {str(postId)}, последний ID - {str(lastPostId)}')
        try:
            await self.bot.copy_message(message.from_user.id, "@RandomFotoChannel", postId, "")
        except():
            await self.send(message)
