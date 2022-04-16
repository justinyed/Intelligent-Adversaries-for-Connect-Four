import sqlite3 as sql
import sqlite3 as Error
import uuid
from datetime import datetime
from uuid import UUID, uuid1
import pandas as pd

sql.register_adapter(UUID, lambda u: u.bytes_le)
sql.register_converter('GUID', lambda b: UUID(bytes_le=b))

DATABASE = "./leaderboard.db"
MEMORY = ":memory:"


class Leaderboard:

    def __init__(self, db_file):
        self.path = db_file
        self.connection = Leaderboard.create_connection(db_file)
        self._initialize_leaderboard()

    @staticmethod
    def create_connection(db_file=DATABASE):
        """
        create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        connection = None
        try:
            print(f"Connecting to {db_file}...")
            connection = sql.connect(db_file)
            print(f"Successfully Connected with sqlite3 version {sql.version}")
        except Error as e:
            print(e)
        return connection

    def create_table(self, create_table_sql):
        """
        create a table from the create_table_sql statement
        :param create_table_sql: a CREATE TABLE statement
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
        except Error as e:
            print(e)

    def __del__(self):
        try:
            self.connection.close()
        except Error as e:
            print(e)

    def add_player(self, player_id):
        now = datetime.now()

        sql = "INSERT OR IGNORE INTO players(player_id, win_amount, loss_amount, tie_amount, games_played, begin_date)" \
              "VALUES(?,?,?,?,?,?)"

        cursor = self.connection.cursor()
        cursor.execute(sql, (player_id, 0, 0, 0, 0, now.strftime("%d/%m/%Y %H:%M:%S")))
        self.connection.commit()
        return cursor.lastrowid

    def update_player(self, player_id, is_win, is_tie):
        cursor = self.connection.cursor()
        cursor.execute("SELECT win_amount, loss_amount, tie_amount, games_played FROM players WHERE player_id=?",
                       (player_id,))
        l = cursor.fetchall()
        win, loss, tie, played = l[0]

        if is_tie and is_win:
            raise ValueError("is_tie and is_win can not both be true!")

        if is_tie:
            tie += 1
        elif is_win:
            win += 1
        else:
            loss += 1

        sql = \
            """UPDATE players
                SET 
                    win_amount = ?,
                    loss_amount = ?,
                    tie_amount = ?,
                    games_played = ?
                WHERE player_id = ?
            """

        cursor = self.connection.cursor()
        cursor.execute(sql, (win, loss, tie, played + 1, player_id))
        self.connection.commit()

    def add_game(self, uid, challenger: str, opponent: str, player1: str, player2: str):
        now = datetime.now()

        sql = "INSERT OR IGNORE INTO games(id,challenger,opponent,player1,player2,status_id,begin_date,moves,turns" \
              ") VALUES(?,?,?,?,?,?,?,?,?)"

        cursor = self.connection.cursor()
        cursor.execute(sql, (uid, challenger, opponent, player1, player2, 0, now.strftime("%d/%m/%Y %H:%M:%S"), "", 0))
        self.connection.commit()
        return cursor.lastrowid

    def update_move(self, uid, move):
        cursor = self.connection.cursor()
        cursor.execute("SELECT turns, moves FROM games WHERE id=?", (uid,))
        l = cursor.fetchall()
        turns, moves = l[0]

        sql = \
            """UPDATE games
                SET 
                    turns = ?,
                    moves = ?
                WHERE id = ?
            """

        cursor = self.connection.cursor()
        cursor.execute(sql, (turns + 1, moves + str(move), uid))
        self.connection.commit()

    def end_game(self, uid, winner, status_id):
        now = datetime.now()
        end = now.strftime("%d/%m/%Y %H:%M:%S")
        sql = \
            """UPDATE games
                SET 
                    status_id = ?,
                    winner = ?,
                    end_date = ?
                WHERE id = ?
            """
        cursor = self.connection.cursor()
        cursor.execute(sql, (status_id, winner, end, uid))
        self.connection.commit()

    def _initialize_leaderboard(self):
        sql_create_table_player = """CREATE TABLE IF NOT EXISTS players (
                                            player_id text PRIMARY KEY,
                                            win_amount integer,
                                            loss_amount integer,
                                            tie_amount integer,
                                            games_played integer,
                                            begin_date text,
                                            UNIQUE(player_id)
                                    );"""

        sql_create_table_games = """CREATE TABLE IF NOT EXISTS games (
                                        id GUID PRIMARY KEY,
                                        challenger text,
                                        opponent text NOT NULL,
                                        player1 text NOT NULL,
                                        player2 text NOT NULL,
                                        status_id integer NOT NULL,
                                        begin_date text NOT NULL,
                                        winner text,
                                        turns integer,
                                        moves text,
                                        end_date text,
                                        UNIQUE(id)
                                    );"""
        self.create_table(sql_create_table_player)
        self.create_table(sql_create_table_games)


if __name__ == '__main__':
    lb = Leaderboard(DATABASE)
    g = uuid1()
    lb.add_game(g, "justinyedinak", "spartanyed", "justinyedinak", "spartanyed")
    lb.update_move(g, 1)
    lb.update_move(g, 4)
    lb.update_move(g, 6)
    lb.end_game(g, 2, 'spartanyed')
