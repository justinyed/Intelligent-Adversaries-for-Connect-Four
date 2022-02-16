import discord
import os
from discord.ext import commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CALLSIGN = "c4 "
bot = commands.Bot(command_prefix=CALLSIGN)

ONE = u"\u2474"
TWO = u"\u2475"
THREE = u"\u2476"
FOUR = u"\u2477"
FIVE = u"\u2478"
SIX = u"\u2479"
SEVEN = u"\u247A"


# This event triggers when your bot
# allows the bot to sit in a ready state and wait for calls.
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{bot.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


@bot.command(name='challenge',
             aliases=['clg'],
             brief='brief',
             description='Challenge a player or agent by providing the ID.  If no parameter is given, then a menu '
                         'will assist.',
             help='help'
             )
async def challenge(ctx, player=None):
    if player is None:
        await ctx.send("Print Default Challenge Dialog")
    else:
        await ctx.send(f"Challenge {player}")


@bot.command(name="leaderboard",
             aliases=['lb'],
             brief='brief',
             description='Display the record for a player or agent by providing the ID. If no parameter is given, '
                         'then a default leaderboard will be displayed.',
             help='help'
             )
async def leaderboard(ctx, player=None):
    if player is None:
        await ctx.send("Print Default Leaderboard")
    else:
        await ctx.send(f"Display {player}'s Record")


class ConnectFourBot:
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(pass_context=True)
    async def cfb(self, ctx, move=""):
        """Connect Four"""
        await self.cfb_new(ctx.message.author, ctx.message.channel)

    async def cfb_new(self, user, channel):
        response = self.cfb_make_board(user)
        response += "Your move:"
        msg = await self.bot.send_message(channel, response)
        await self.make_buttons(msg)

    async def make_buttons(self, msg):
        await self.bot.add_reaction(msg, ONE)
        await self.bot.add_reaction(msg, TWO)
        await self.bot.add_reaction(msg, THREE)
        await self.bot.add_reaction(msg, FOUR)
        await self.bot.add_reaction(msg, FIVE)
        await self.bot.add_reaction(msg, SIX)
        await self.bot.add_reaction(msg, SEVEN)

    def cfb_make_board(self, user):
        pass

    async def game_handler(self, game):
        pass

    async def challenge_handler(self):
        pass

    async def leaderboard_handler(self):
        pass


bot.run(DISCORD_TOKEN)
