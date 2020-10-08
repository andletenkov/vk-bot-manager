import asyncio

from loguru import logger


class BotRunner(object):
    _bots = []

    def __init__(self, *bots):
        for bot in bots:
            self.register_bot(bot)

    def register_bot(self, bot):
        self._bots.append(bot)

    def run(self):
        raise NotImplementedError


class AsyncRunner(BotRunner):

    async def main(self):
        tasks = [asyncio.create_task(bot.listen()) for bot in self._bots]
        await asyncio.gather(*tasks)

    def run(self):
        try:
            asyncio.run(self.main())
        except (KeyboardInterrupt, SystemExit):
            logger.info('Exit')
