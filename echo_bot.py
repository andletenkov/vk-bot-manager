"""
Example implementation of bot that echoes received message
"""
import random

from decorators import on_message_new
from async_ import AsyncLongPollBot
from config import ECHO_ID, ECHO_TOKEN

echo_bot = AsyncLongPollBot(__name__, ECHO_ID, ECHO_TOKEN)


@on_message_new(echo_bot, ['/hello', '/hi'])
def echo(vk, event):
    reply_to = event['object']['from_id']
    text = event['object']['text']
    vk.messages.send(user_id=reply_to, message=text,
                     random_id=random.randint(1, 10000))
