"""
Example implementation of bot that says "It's Wednesday" to his dudes
"""
import random

from enums import VkEventType
from bots import AsyncLongpollBot
from config import DUDE_ID, DUDE_TOKEN

dude_bot = AsyncLongpollBot(__name__, DUDE_ID, DUDE_TOKEN)


@dude_bot.callback(VkEventType.MESSAGE_NEW)
def reply(vk, event):
    reply_to = event['object']['from_id']
    vk.messages.send(user_id=reply_to, message="It's Wednesday, my dudes.",
                     random_id=random.randint(1, 10000))
