from typing import Callable

from loguru import logger

from enums import VkEventType
from vk_api import VK


class Bot(object):

    def __init__(self, name: str, token: str):
        self.vk = VK(token)
        self.name = name
        self._handlers = {}

    def add_handler(self, event_type: VkEventType, func: Callable):
        handlers = self._handlers.get(event_type.value)
        if handlers:
            handlers.append(func)
        else:
            self._handlers[event_type.value] = [func]

    def get_handlers(self, event_type: str):
        try:
            return self._handlers[event_type]
        except KeyError:
            logger.warning(f'No handler for "{event_type}" event')

    def listen(self):
        raise NotImplementedError


class Runner(object):
    _bots = None

    def __init__(self, *bots: Bot):
        self._bots = list(bots) if bots else []
        for bot in bots:
            self.register_bot(bot)

    def register_bot(self, bot: Bot):
        self._bots.append(bot)

    def run(self):
        raise NotImplementedError
