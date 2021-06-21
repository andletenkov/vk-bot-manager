import functools
import inspect
import re
from typing import List

from base import Bot
from enums import VkEventType


def on_message_new(bot: Bot, phrases: List[str]):
    def wrapper(f):

        @functools.wraps(f)
        async def inner(vk, event):
            text = event['object']['message']['text']

            for pattern in phrases:
                reg_exp = re.compile(pattern)
                if reg_exp.match(text):

                    if inspect.iscoroutinefunction(f):
                        return await f(vk, event)
                    return f(vk, event)

        bot.add_handler(VkEventType.MESSAGE_NEW, inner)

        return inner

    return wrapper
