class Player:

    def __init__(self, user_id: str, player_number: int, bot=False):
        self._user_id = user_id
        self._bot = bot
        self._player_number = player_number

    async def get_action(self):
        pass
