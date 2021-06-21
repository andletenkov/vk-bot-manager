import asyncio
import aiohttp

from base import Bot, Runner
from loguru import logger


class AsyncLongPollBot(Bot):

    def __init__(self, name: str, group_id: int, token: str, wait=25):
        super().__init__(name, token)
        self.group_id = group_id
        self.wait = wait

        self.session = None
        self.server = None
        self.key = None
        self.ts = None

    def get_server(self, update_ts: bool = True):
        response_obj = self.vk.groups.getLongPollServer(group_id=self.group_id)
        try:
            response = response_obj['response']
            self.key = response['key']
            self.server = response['server']

            if update_ts:
                self.ts = response['ts']
        except KeyError:
            logger.error(f'Cannot parse response: {response_obj}')

    async def poll(self, params):
        if self.session is None:
            self.session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False),
                raise_for_status=True
            )
        response = await self.session.get(
            self.server,
            params=params,
            timeout=self.wait + 10
        )
        return await response.json()

    async def get_updates(self):
        params = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
        }

        json = await self.poll(params)

        if 'failed' not in json:
            self.ts = json['ts']
            return json['updates']

        elif json['failed'] == 1:
            self.ts = json['ts']

        elif json['failed'] == 2:
            self.get_server(update_ts=False)

        elif json['failed'] == 3:
            self.get_server()

        else:
            logger.error(f'[{self.name}] Unable to handle response: {json}')

        return []

    async def stop(self):
        if self.session:
            logger.info(f'[{self.name}] Closing client session...')
            await self.session.close()

    async def start(self):
        self.get_server()
        if self.server:
            logger.info(f'[{self.name}] Started and running')
            await self.listen()

    async def listen(self):
        while True:
            events = await self.get_updates()
            for event in events:
                logger.info(f'[{self.name}] New event: {event}')

                handlers = self.get_handlers(event['type'])

                if handlers:
                    try:
                        for handler in handlers:
                            await handler(self.vk, event)
                    except Exception as e:
                        logger.error(f'[{self.name}] Error: {e}')


class AsyncRunner(Runner):

    async def main(self):
        tasks = [asyncio.create_task(bot.start()) for bot in self._bots]
        await asyncio.gather(*tasks)

    async def shutdown(self):
        shutdown_tasks = []
        for bot in self._bots:
            shutdown_tasks.append(asyncio.create_task(bot.stop()))
        closing_session_futures = asyncio.gather(*shutdown_tasks)
        await closing_session_futures
        logger.info('Exited')

    def run(self):
        try:
            asyncio.run(self.main())
        except (KeyboardInterrupt, SystemExit):
            asyncio.run(self.shutdown())
