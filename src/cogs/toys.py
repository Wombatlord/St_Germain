import random
from discord.ext import commands
from discord.ext.commands import Context


class Toy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx: Context, left: int, right: int):
        # Adds two numbers
        result = str(left + right)
        await ctx.send(result)

    @commands.command()
    async def magicEight(self, ctx: Context, message='question'):
        if message:
            eightBall = random.randint(0, 19)
            outlooks = [
                "As I see it, yes.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don’t count on it.",
                "It is certain.",
                "It is decidedly so.",
                "Most likely.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Outlook good.",
                "Reply hazy, try again.",
                "Signs point to yes.",
                "Very doubtful.",
                "Without a doubt.",
                "Yes.",
                "Yes – definitely.",
                "You may rely on it.",
            ]
            await ctx.send('Magic 8: ' + outlooks[eightBall])


def setup(bot):
    bot.add_cog(Toy(bot))
