"""
Example implementation of bot that says "It's Wednesday" to his dudes
"""
import random

from decorators import on_message_new
from async_ import AsyncLongPollBot
from config import DUDE_ID, DUDE_TOKEN

dude_bot = AsyncLongPollBot(__name__, DUDE_ID, DUDE_TOKEN)


@on_message_new(dude_bot, ['/hello', 'hi'])
def reply(vk, event):
    reply_to = event['object']['from_id']
    vk.messages.send(user_id=reply_to, message="It's Wednesday, my dudes.",
                     random_id=random.randint(1, 10000))
