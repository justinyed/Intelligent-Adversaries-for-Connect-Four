import os
from random import shuffle
from discord.ext import commands
import discord_bot.constants_discord as constant
import time


class Utilities(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[Utilities Initialized]")

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket latency"""
        start_time = time.time()
        message = await ctx.send("Testing Ping...", delete_after=5)
        end_time = time.time()
        await message.edit(
            content=f"Online! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    @commands.command(name='clean', pass_context=True)
    async def clean(self, ctx: commands.Context):
        if str(ctx.author) in constant.ADMINS:
            await ctx.channel.purge()
        else:
            await ctx.send("You do not have permission for this command", delete_after=3)

    @staticmethod
    def setup(bot: commands.Bot):
        bot.add_cog(Utilities(bot))
