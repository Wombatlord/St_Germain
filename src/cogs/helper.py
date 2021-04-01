from discord.ext import commands
from discord.ext.commands import Context


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tarotGuide = "```" + "The following commands are available. If a command has no example, send it alone.\n" \
                         "Tarot / Meaning / Describe / Image are only available in The White Lodge. \n\n" \
                         "!add: Adds two numbers together. !add 284 382\n\n" \
                         "!magicEight: A Magic Eight ball.\n\n" \
                         "!magicEight: Presents a magicEight spread of up to 7 cards. !magicEight 5\n\n" \
                         "!meaning: Presents the Normal & Reversed meaning of a card. !meaning Magician\n\n" \
                         "!describe: Presents the description of a card. !describe High Priestess\n\n" \
                         "!image: Presents the image of a card. !image Tower" + "```"

    @commands.command()
    async def guidance(self, ctx: Context):
        await ctx.send(self.tarotGuide)
