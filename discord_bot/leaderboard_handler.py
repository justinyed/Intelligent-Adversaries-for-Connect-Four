import discord
import asyncio
from discord.ext import commands
from discord import Button, ButtonStyle, ActionRow, SelectMenu, SelectOption
import discord_constants as constant
import tabulate
from record import Record


class LeaderBoardHandler(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[LeaderBoardHandler Initialized]")

    @commands.command(name='leaderboard', aliases=['lb', 'record'],
                      description=constant.LB_DESCRIPTION, help='help', pass_contaxt=True)
    async def leaderboard(self, ctx: commands.Context, num_entries=10):
        """
        Displays a leaderboard
        :param ctx: context
        :param num_entries:
        """
        msg = await ctx.send("Leaderboard is Loading")
        author = ctx.author

        #  retrieve and display top num_entries

    @commands.command(name='record', aliases=['rec'],
                      description=constant.REC_DESCRIPTION, help='help', pass_contaxt=True)
    async def record(self, ctx: commands.Context, *players):
        """
        Displays the Record of a player or players
        :param ctx: context
        :param players:
        """
        msg = await ctx.send("Record is Loading")
        author = ctx.author
        if players is None:
            pass
            #  Display author's record
        else:
            pass
            # Display players records

    @staticmethod
    def setup(bot: commands.Bot):
        bot.add_cog(LeaderBoardHandler(bot))
