from sqlite3 import Error

import discord
import asyncio
from discord.ext import commands
import discord_config as constant
from leaderboard_database import Leaderboard


class LeaderBoardHandler(commands.Cog):

    def __init__(self, bot: commands.Bot, leaderboard):
        try:
            self.leaderboard = leaderboard
        except Error as e:
            print("Failed to Load Database from file:", leaderboard.path)
            print(e)
        self.bot = bot
        print("[LeaderBoardHandler Initialized]")

    @commands.command(name='leaderboard', aliases=['lb', 'record'], pass_contaxt=True)
    async def view_leaderboard(self, ctx: commands.Context, num_entries=10):
        """
        Displays a leaderboard
        :param ctx: context
        :param num_entries:
        """
        msg = await ctx.send("Leaderboard is Loading")
        author = ctx.author

        #  retrieve and display top num_entries

    # @commands.command(name='record', aliases=['rec'], pass_contaxt=True)
    # async def record(self, ctx: commands.Context, *players):
    #     """
    #     Displays the Record of a player or players
    #     :param ctx: context
    #     :param players:
    #     """
    #     msg = await ctx.send("Record is Loading")
    #     author = ctx.author
    #     if players is None:
    #         pass
    #         #  Display author's record
    #     else:
    #         pass
    #         # Display players records

    async def add_player(self, player_id):
        self.leaderboard.add_player(player_id)

    async def update_player(self, player_id, is_win, is_tie=False):
        self.leaderboard.update_player(player_id, is_win, is_tie)

    async def add_game(self, uid, challenger, opponent, player1, player2):
        self.leaderboard.add_game(uid, challenger, opponent, player1, player2)

    async def update_move(self, uid, move):
        self.leaderboard.update_move(uid, move)

    async def end_game(self, uid, winner, status):
        self.leaderboard.end_game(uid, winner, status)

    @staticmethod
    def setup(bot: commands.Bot, db_file):
        lh = LeaderBoardHandler(bot, db_file)
        bot.add_cog(lh)
        return lh
