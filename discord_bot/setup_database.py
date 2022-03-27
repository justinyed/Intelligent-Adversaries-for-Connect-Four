import sqlite3 as sl

con = sl.connect('my-test.db')

with con:
    con.execute("""
        CREATE TABLE USER (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            wins INTEGER,
            losses INTEGER,
            ties INTEGER,
            win_loss_rate FLOAT,
            date_added DATE,
            date_last_played DATE
        );
    """)
    con.execute("""
            CREATE TABLE GAME (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                end_status INTEGER,
                moves TEXT,
                player1 TEXT,
                player2 TEXT,
                time_begin DATE,
                time_end DATE
            );
        """)
