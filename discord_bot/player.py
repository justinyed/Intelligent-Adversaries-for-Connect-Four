import discord
from discord_bot import constants_discord as constant

class Player:

    def __init__(self, user_id: str, player_number: int, bot=False, intelligence=None):
        self._user_id = user_id
        self._bot = bot
        self._intelligence = intelligence
        self._player_number = player_number

    def get_user_id(self):
        return self._user_id

    async def get_action(self, game):
        """
        The Agent will receive a game and must return an action from the legal moves

        :param game: current state of the game
        :return: The action chosen by the agent given the game
        """
        if not self._bot:


    async def assemble_buttons(self, msg: discord.Message):
        """
        Create reaction buttons
        :param msg:
        :return:
        """
        for button in constant.BUTTON_NUMBERS:
            await msg.add_reaction(button)

    async def on_reaction_add(self, bot, reaction, challenger):
        """

        :param reaction:
        :param challenger:
        :return:
        """
        opponent = ""
        if reaction.message.author.id == bot.user.id and not challenger.id == bot.user.id:
            move = constant.BUTTON_DECODER[(str(reaction.emoji))]
            if move is not None:
                await self.game_handler(challenger, opponent, reaction.message, move)



