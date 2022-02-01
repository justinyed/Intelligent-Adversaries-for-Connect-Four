import os
import random
import discord
import argparse

token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")
parser = argparse.ArgumentParser()

# Setup Intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
callsign = "@c4"

# This event triggers when your bot
# allows the bot to sit in a ready state and wait for calls. 
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content.lower()

    if message_content.startswith(callsign):




        parameters = message_content.split(" ")
        cmd = parameters[1]


        await message.channel.send("")


class get_parser:
    def __init__(self):
        # create parser object
        self.parser = argparse.ArgumentParser(description="A connect 4 bot")

        # defining arguments for parser object
        self.parser.add_argument("play", "challenge", )




# tell the client to run when the script is executed using your API token
client.run(token)
