import discord
from discord.ext import commands
import asyncio
import discord_config as config
from discord_config import MESSAGE, TIME


class HelpHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[Help Initialized]")

    @commands.command(name='info', aliases=['h'], pass_contaxt=True)
    async def help(self, ctx: commands.Context):
        """
        Give information about the discord bot's functions
        :param ctx: context
        """
        await ctx.send("Help Information", embed=discord.Embed())

    @staticmethod
    def setup(bot: commands.Bot):
        bot.add_cog(HelpHandler(bot))

