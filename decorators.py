import functools
import re
from typing import List

from base import Bot
from enums import VkEventType


def on_message_new(bot: Bot, phrases: List[str]):
    def wrapper(f):
        bot.add_handler(VkEventType.MESSAGE_NEW, f)

        @functools.wraps
        def inner(vk, event):
            text = event['object']['text']

            for pattern in phrases:
                reg_exp = re.compile(pattern)
                if reg_exp.match(text):
                    return f(vk, event)

        return inner

    return wrapper
