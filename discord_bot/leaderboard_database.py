from sqlite3 import Error
import sqlite3 as sql
from datetime import datetime
from uuid import UUID
import pandas as pd


sql.register_adapter(UUID, lambda u: u.bytes_le)
sql.register_converter('GUID', lambda b: UUID(bytes_le=b))

MEMORY = ":memory:"
in_progress = 'in_progress'
dt_format = "%d/%m/%Y %H:%M:%S"
rounding = 3


class Leaderboard:

    def __init__(self, db_file):
        self.path = db_file
        self.connection = Leaderboard.create_connection(db_file)
        self._initialize_leaderboard()

    @staticmethod
    def create_connection(db_file):
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
            print(f"Couldn't Connect using path {db_file}")
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
        print("Disconnecting from the Database...")
        self.connection.close()
        print("Successfully Disconnected.")

    def get_player(self, player_id):
        try:
            sql = f"SELECT * FROM players WHERE player_id={player_id}"
            return pd.read_sql_query(sql, self.connection)
        except Error as e:
            print(e)
            return None

    def get_top_players(self, k):
        try:
            sql = f"SELECT * FROM players ORDER BY win_rate LIMIT {k}"
            return pd.read_sql_query(sql, self.connection)
        except Error as e:
            print(e)
            return None

    def add_player(self, player_id):
        now = datetime.now()
        date = now.strftime(dt_format)

        sql = "INSERT OR IGNORE INTO players(player_id, win_amount, loss_amount, " \
              "tie_amount, games_played, begin_date, last_date, win_rate, loss_rate, tie_rate, win_loss_rate) " \
              "VALUES(?,?,?,?,?,?,?,?,?,?,?)"

        cursor = self.connection.cursor()
        cursor.execute(sql, (player_id, 0, 0, 0, 0, date, date, 0.0, 0.0, 0.0, 0.0))
        self.connection.commit()
        return cursor.lastrowid

    def update_player(self, player_id, is_win, is_tie=False):
        now = datetime.now()
        date = now.strftime(dt_format)

        cursor = self.connection.cursor()
        cursor.execute("SELECT win_amount, loss_amount, tie_amount, games_played FROM players WHERE player_id=?",
                       (player_id,))
        retrieved = cursor.fetchall()
        win, loss, tie, played = retrieved[0]

        if is_tie and is_win:
            raise ValueError("is_tie and is_win can not both be true!")

        played += 1

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
                    games_played = ?,
                    last_date = ?,
                    win_rate = ?,
                    loss_rate = ?,
                    tie_rate = ?,
                    win_loss_rate = ?
                WHERE player_id = ?
            """

        if loss != 0.0:
            win_loss_rate = round(win / loss, rounding)
        else:
            win_loss_rate = 0.0

        cursor = self.connection.cursor()
        cursor.execute(
            sql,
            (
                win, loss, tie, played, date,
                round(win / played, rounding), round(loss / played, rounding),
                round(tie / played, rounding), win_loss_rate,
                player_id,
            )
        )
        self.connection.commit()

    def add_game(self, uid, player1: str, player2: str):
        now = datetime.now()

        sql = "INSERT OR IGNORE INTO games(id,player1,player2,status_id,begin_date,moves,turns," \
              "winner,end_date" \
              ") VALUES(?,?,?,?,?,?,?,?,?)"

        cursor = self.connection.cursor()

        cursor.execute(
            sql,
            (uid, player1, player2, 0, now.strftime(dt_format), "", 0, in_progress,
             in_progress),
        )

        self.connection.commit()
        return cursor.lastrowid

    def update_move(self, uid, move):
        cursor = self.connection.cursor()
        cursor.execute("SELECT turns, moves FROM games WHERE id=?", (uid,))
        retrieved = cursor.fetchall()
        turns, moves = retrieved[0]

        sql = \
            """UPDATE games
                SET 
                    turns = ?,
                    moves = ?
                WHERE id = ?
            """

        cursor.execute(sql, (turns + 1, moves + str(move), uid))
        self.connection.commit()

    def end_game(self, uid, winner, status_id):
        now = datetime.now()
        end = now.strftime(dt_format)
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
                                            win_rate float,
                                            loss_rate float,
                                            tie_rate float,
                                            win_loss_rate float,
                                            begin_date text,
                                            last_date text,
                                            UNIQUE(player_id)
                                    );"""

        sql_create_table_games = """CREATE TABLE IF NOT EXISTS games (
                                        id GUID PRIMARY KEY,
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

    def get_game_start(self, uid):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT begin_date FROM games WHERE id=?", (uid,))
            retrieved = cursor.fetchall()
            start_date = retrieved[0]
            return start_date
        except Error as e:
            print(e)
            return
