import discord
from discord_bot import constants_discord as constant
import intelligence


class Human(intelligence.Agent):

    def __init__(self, player, user_id, message: discord.Message):
        super().__init__(player)
        self._user_id = user_id
        self._message = message

    def get_user_id(self):
        return self._user_id

    async def get_action(self, game):
        """
        The Agent will receive a game and must return an action from the legal moves

        :param game: current state of the game
        :return: The action chosen by the agent given the game
        """
        await self.assemble_buttons()

    async def assemble_buttons(self):
        """
        Create reaction buttons
        :param msg:
        :return:
        """
        for button in constant.BUTTON_NUMBERS:
            await self._message.add_reaction(button)

    async def on_reaction_add(self, reaction, user):
        """
        :param reaction:
        :return:
        """
        if reaction.message.author.id == self.get_user_id():
            move = constant.BUTTON_DECODER[(str(reaction.emoji))]
            if move is not None:
                return move
