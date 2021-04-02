from src.bot.stGermain import bot
from src.server import keepAlive, token

if token.repl is True:
    keepAlive.keepAlive()

bot.run()
