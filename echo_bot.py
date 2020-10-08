"""
Example implementation of bot that echoes received message
"""
import random

from enums import VkEventType
from bots import AsyncLongpollBot
from config import ECHO_ID, ECHO_TOKEN

echo_bot = AsyncLongpollBot(__name__, ECHO_ID, ECHO_TOKEN)


@echo_bot.callback(VkEventType.MESSAGE_NEW)
def echo(vk, event):
    reply_to = event['object']['from_id']
    text = event['object']['text']
    vk.messages.send(user_id=reply_to, message=text,
                     random_id=random.randint(1, 10000))
