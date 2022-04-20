import asyncio
import os
from sqlite3 import Error

import discord
import matplotlib.pyplot as plt
from discord.ext import commands

from discord_bot.leaderboard_database import Leaderboard

path = "./media/leaderboard.png"
dt_format = "%d/%m/%Y %H:%M:%S"


def save_df_as_image(df, path):
    fig, ax = plt.subplots(frameon=False)
    ax.set_axis_off()  # remove the axis
    plt.box(False)
    fig.subplots_adjust(top=0.001, bottom=0)

    columns = [
        "player_id", "win_loss_rate", "games_played",
        "win_rate", "loss_rate", "tie_rate",
        "win_amount", "loss_amount", "tie_amount"
    ]

    columns_labels = [
        "Player", "Win Loss Rate", "Games Played",
        "Win Rate", "Loss Rate", "Tie Rate",
        "Wins", "losses", "Ties"
    ]

    table = ax.table(
        cellText=df[columns].values,
        colLabels=columns_labels,
        rowLabels=[f" {i + 1:3d} " for i in range(len(df.index))],
        rowColours=["royalblue"] * len(df.index),
        colColours=["royalblue"] * len(columns),
        loc='center',
    )

    table.set_fontsize(14)
    table.scale(4, 4)
    plt.savefig(path, bbox_inches='tight', dpi=128, pad_inches=0)


class LeaderBoardHandler(commands.Cog):

    def __init__(self, bot: commands.Bot, leaderboard: Leaderboard):
        try:
            self.leaderboard = leaderboard
        except Error as e:
            print("Failed to Load Database from file:", leaderboard.path)
            print(e)
        self.bot = bot
        self.changed = True
        print("[LeaderBoardHandler Initialized]")

    @commands.command(name='leaderboard', aliases=['lb', 'record'], pass_contaxt=True)
    async def view_leaderboard(self, ctx: commands.Context, num_entries=10):
        """
        Displays a leaderboard
        :param ctx: context
        :param num_entries:
        """
        msg = await ctx.send("Leaderboard is Loading...")

        if self.changed:
            df = self.leaderboard.get_top_players(num_entries)
            save_df_as_image(df, path)
            self.changed = False

        try:
            if not os.path.isfile(path):
                raise FileNotFoundError(f"File not found at {path}")

            with open(path, 'rb') as f:
                picture = discord.File(f, filename="lb.png")
                await msg.delete()
                await ctx.send(content="Click on the Leaderboard below to View:", file=picture, delete_after=20)

        except Exception as e:
            await msg.edit(content="Leaderboard Failed to Load.", delete_after=5)
            print(e)

    async def update_player(self, player_id: str, is_win, is_tie=False):
        self.leaderboard.update_player(player_id, is_win, is_tie)

    async def add_game(self, uid, player1: str, player2: str):
        self.leaderboard.add_player(player1)
        self.leaderboard.add_player(player2)
        self.leaderboard.add_game(uid, player1, player2)

    async def update_move(self, uid, move):
        self.leaderboard.update_move(uid, move)

    async def end_game(self, uid, winner, loser, status, is_tied=False):
        self.changed = True

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
