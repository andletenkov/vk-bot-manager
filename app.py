from async_ import AsyncRunner

from echo_bot import echo_bot
from dude_bot import dude_bot

if __name__ == '__main__':
    app = AsyncRunner()
    app.register_bot(echo_bot)
    app.register_bot(dude_bot)
    app.run()
