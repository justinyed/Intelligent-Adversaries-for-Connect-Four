import discord
from challenge_handler import ChallengeHandler
from util import Util
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
ChallengeHandler.setup(bot)
TOKEN = Util.read_json_from_file("./discord_bot/connect_four_config.json")['Token']
bot.run(TOKEN)
