from datetime import datetime
import json
import os

file = "./discord_bot/records.json"


class Record:

    def __init__(self, player1: str, player2: str, time_begin=datetime.now(), moves=None, time_end=None,
                 end_status=None):
        if moves is None:
            moves = []
        self._player1 = str(player1)
        self._player2 = str(player2)
        self._time_begin = time_begin
        self._moves = moves
        self._time_end = time_end
        self._end_status = end_status

    def add_move(self, move: int):
        self._moves.append(move)

    def game_finished(self, end_status: int):
        self._time_end = datetime.now()
        self._end_status = end_status

    def get_time(self):
        return self._time_begin

    def get_moves(self):
        return self._moves

    def get_player1(self):
        return self._player1

    def get_player2(self):
        return self._player2

    def get_end_status(self):
        return self._end_status

    def get_winner(self):
        if self._end_status == 3:
            return None
        if self._end_status == 1:
            return self._player1
        else:
            return self._player2

    def to_dictionary(self):
        return {
            'player1': self._player1,
            'player2': self._player2,
            'time_begin': str(self._time_begin),
            'moves': self._moves,
            'time_end': str(self._time_end),
            'end_status': self._end_status
        }

    @staticmethod
    def from_dictionary(d: dict):
        return Record(*d.values())

    async def save(self):
        key = f"{self._time_begin.strftime('%d-%m-%Y_%H:%M:%S')},{self._player1},{self._player2}"
        try:
            if not os.path.isfile(file):
                with open(file, "w") as write:
                    json.dump({key: self.to_dictionary()}, fp=write, sort_keys=True, indent=2)
            else:
                with open(file, "r") as read:
                    data = json.load(read)
                data[key] = self.to_dictionary()
                with open(file, "w") as write:
                    json.dump(data, fp=write, sort_keys=True, indent=2)
        except FileNotFoundError:
            print("File not Found.")
            return
        except IOError:
            print("IO Error")
            return
        print("Record Saved Successfully")
