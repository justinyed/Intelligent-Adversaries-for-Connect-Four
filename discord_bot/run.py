import discord
from discord.ext import commands
from challenge_handler import ChallengeHandler
from utilities import Utilities
from json_utilities import Util

discord.MemberCacheFlags.all()
intents = discord.Intents(messages=True, guilds=True)

bot = commands.Bot(command_prefix="!", intents=intents)
ChallengeHandler.setup(bot)
Utilities.setup(bot)
TOKEN = Util.read_json_from_file("./discord_bot/connect_four_config.json")['Token']
bot.run(TOKEN)
