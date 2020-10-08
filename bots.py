import aiohttp
import functools
from loguru import logger
from vk_api import VK


class Bot(object):

    def __init__(self, name, token):
        self.vk = VK(token)
        self.name = name
        self._callbacks = {}

    def callback(self, event_type):
        def wrapper(f):
            self._add_callback(event_type, f)

            @functools.wraps
            def inner(*args, **kwargs):
                return f(*args, **kwargs)

            return inner

        return wrapper

    def _add_callback(self, event_type, func):
        self._callbacks[event_type.value] = func

    def get_callback(self, event_type):
        try:
            return self._callbacks[event_type]
        except KeyError:
            logger.error(f'No handler for "{event_type}" event')

    def listen(self):
        raise NotImplementedError


class AsyncLongpollBot(Bot):

    def __init__(self, name, group_id, token, wait=25):
        super().__init__(name, token)
        self.group_id = group_id
        self.wait = wait

        self.server = None
        self.key = None
        self.ts = None

        self.get_server()

    def get_server(self, update_ts=True):
        response_obj = self.vk.groups.getLongPollServer(group_id=self.group_id)
        try:
            response = response_obj['response']
            self.key = response['key']
            self.server = response['server']

            if update_ts:
                self.ts = response['ts']
        except KeyError:
            logger.error(f'Cannot parse response: {response_obj}')

    async def get_updates(self):

        params = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
        }

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(
                    self.server,
                    params=params,
                    timeout=self.wait + 10
            ) as response:
                json = await response.json()

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
            logger.error(f'Unable to handle response: {response}')

        return []

    async def listen(self):
        while True:
            events = await self.get_updates()
            for event in events:
                logger.info(f'[{self.name}] New event: {event}')

                callback = self.get_callback(event['type'])
                callback(self.vk, event)
