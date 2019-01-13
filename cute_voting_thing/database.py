import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created.")
    except Error as e:
        print(e)

def main():
    database = "cvt.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        password text NOT NULL
                                    ); """

    sql_create_musics_table = """ CREATE TABLE IF NOT EXISTS musics (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        artist text
                                    ); """

    sql_create_polls_table = """ CREATE TABLE IF NOT EXISTS polls (
                                        id integer PRIMARY KEY,
                                        begin_date text NOT NULL,
                                        end_date text NOT NULL,
                                        user_id integer NOT NULL,
                                        music_a_id integer NOT NULL,
                                        music_b_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (id),
                                        FOREIGN KEY (music_a_id) REFERENCES musics (id),
                                        FOREIGN KEY (music_b_id) REFERENCES musics (id)
                                    ); """

    sql_create_votes_table = """ CREATE TABLE IF NOT EXISTS votes (
                                        id integer PRIMARY KEY,
                                        poll_id integer NOT NULL,
                                        chosen_music_id integer NOT NULL,
                                        FOREIGN KEY (poll_id) REFERENCES polls (id),
                                        FOREIGN KEY (chosen_music_id) REFERENCES musics (id)
                                    ); """

    tables = [sql_create_users_table, sql_create_musics_table, sql_create_polls_table, sql_create_votes_table]
    conn = create_connection(database)

    if conn is not None:
        for table in tables:
            create_table(conn, table)
    else:
        print("Error! Cannot create the database connection.")


if __name__ == '__main__':
    main()
