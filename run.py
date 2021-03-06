import discord
from discord.ext import commands
from discord_bot.challenge_handler import ChallengeHandler
from discord_bot.leaderboard_handler import LeaderBoardHandler
from discord_bot.help_handler import HelpHandler
from discord_bot.utilities import Utilities
from discord_bot.json_utilities import Util
from discord_bot.leaderboard_database import Leaderboard

discord.MemberCacheFlags.all()
intents = discord.Intents(messages=True, guilds=True)

db_file = './data/leaderboard.db'
leaderboard = Leaderboard(db_file)
bot = commands.Bot(command_prefix="!", intents=intents)

# Load Cogs
lh = LeaderBoardHandler.setup(bot, leaderboard)
ChallengeHandler.setup(bot, lh)
HelpHandler.setup(bot)
Utilities.setup(bot)

TOKEN = Util.read_json_from_file("./discord_bot/token.json")['Token']
bot.run(TOKEN)
