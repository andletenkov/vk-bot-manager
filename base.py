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


class Runner(object):
    _bots = None

    def __init__(self, *bots):
        self._bots = list(bots) if bots else []
        for bot in bots:
            self.register_bot(bot)

    def register_bot(self, bot):
        self._bots.append(bot)

    def run(self):
        raise NotImplementedError
