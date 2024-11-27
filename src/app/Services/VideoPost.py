from .BaseService import BaseService
from app.Confs.TgApiConf import videoCannel


class Video(BaseService):
    async def save(self, message):
        messageId = await self.bot.copy_message(
            chat_id=videoCannel,
            from_chat_id=message.from_user.id,
            message_id=message.message_id,
            caption=str(message.from_user.id)
        )
        self.postRepository.savePost(self.postRepository.video_type, messageId.message_id)

    async def send(self, message):
        lastPostId = self.postRepository.getLastPostByType(self.postRepository.video_type)
        lastPostId = lastPostId[self.postRepository.field_entity_id]

        firstPostId = self.postRepository.getFirstPostByType(self.postRepository.video_type)
        firstPostId = firstPostId[self.postRepository.field_entity_id]

        postId = int(self.random.randint(firstPostId, int(lastPostId)))
        curTime = self.time.gmtime(self.time.time() + (60 * 60 * 3))
        curTime = self.time.strftime("%H:%M:%S", curTime)
        await self.logger.writeLog(f'@{str(message.from_user.username)} ({str(message.from_user.id)})-{str(
            curTime)}//ID видео-поста - {str(postId)}, последний ID - {str(lastPostId)}')
        print(f'{str(message.from_user.username)} ({str(message.from_user.id)})-{str(
            curTime)}//ID видео-поста - {str(postId)}, последний ID - {str(lastPostId)}')
        try:
            await self.bot.copy_message(
                chat_id=message.from_user.id,
                from_chat_id=videoCannel,
                message_id=postId,
                caption=' ')
        except():
            await self.send(message)
