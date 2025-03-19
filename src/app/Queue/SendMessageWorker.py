from .WorkerBase import BaseWorker, Message, Bot, Logger

class SendMessageWorker(BaseWorker):
    def __init__(self, queue, bot: Bot, logger: Logger):
        super().__init__(queue, bot, logger)

    async def work(self, queue):
        while True:
            message: Message = await queue.get()
            print('test')