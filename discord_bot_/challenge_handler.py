from discord.ext import commands
from discord_bot import constants_discord as constant


class ChallengeHandler(commands.Cog, name='challenge handler'):
    def __init__(self, bot):
        self.bot = bot
        self._TASKS = dict()
        self._IDLE_MEMBERS = dict()

    @commands.command(name='challenge', aliases=['clg'],
                      description=constant.CLG_DESCRIPTION, help='help', pass_contaxt=True)
    async def challenge(self, ctx, opponent=None):
        """
        Allows the player to challenge an opponent
        :param ctx: context
        :param opponent: opponent player to challenge; if none options are given.
        """
        await ctx.send(f"Challenge {opponent}")
        # if opponent is None:  # Normally print dialog and request more info
        #     opponent = "Alpha-Beta Agent"
        #     await self.cfb_new(ctx.message.author, opponent, ctx.message.channel)
        # else:
        #     await ctx.send(f"Challenge {opponent}")
