from sqlite3 import Error
from discord.ext import commands
from discord_bot.leaderboard_database import Leaderboard


class LeaderBoardHandler(commands.Cog):

    def __init__(self, bot: commands.Bot, leaderboard: Leaderboard):
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

    async def update_player(self, player_id: str, is_win, is_tie=False):
        self.leaderboard.update_player(player_id, is_win, is_tie)

    async def add_game(self, uid, player1: str, player2: str):
        self.leaderboard.add_player(player1)
        self.leaderboard.add_player(player2)
        self.leaderboard.add_game(uid, player1, player2)

    async def update_move(self, uid, move):
        self.leaderboard.update_move(uid, move)

    async def end_game(self, uid, winner, loser, status, is_tied=False):

        if is_tied:
            self.leaderboard.end_game(uid, 'tied', status)
            self.leaderboard.update_player(winner, is_win=False, is_tie=True)
            self.leaderboard.update_player(loser, is_win=False, is_tie=True)
        else:
            self.leaderboard.end_game(uid, winner, status)
            self.leaderboard.update_player(winner, is_win=True, is_tie=False)
            self.leaderboard.update_player(loser, is_win=False, is_tie=False)

    async def get_game_start(self, uid):
        return self.leaderboard.get_game_start(uid)

    @staticmethod
    def setup(bot: commands.Bot, db_file):
        lh = LeaderBoardHandler(bot, db_file)
        bot.add_cog(lh)
        return lh
