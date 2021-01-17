# db setup file

import sqlite3, json
from sqlite3 import Error


def create_connection(database):
    try:
        conn = sqlite3.connect(database, isolation_level=None, check_same_thread=False)
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))

        return conn
    except Error as e:
        print(e)


def create_questions_table(c):
    sql = """
        CREATE TABLE IF NOT EXISTS questions (
            id integer NOT NULL PRIMARY KEY,
            pollid varchar(8) NOT NULL,
            content varchar(255) NOT NULL
        )
    """
    c.execute(sql)


def create_options_table(c):
    sql = """
        CREATE TABLE IF NOT EXISTS options (
            pollid varchar(8) NOT NULL,
            optname varchar(127) NOT NULL
        )
    """
    c.execute(sql)


def get_question_for_pollid(c, pollid):
    sql = """
        SELECT content FROM questions WHERE pollid = ? ORDER BY id DESC LIMIT 1
    """
    cur = c.cursor()
    cur.execute(sql, (pollid,))
    question_content = cur.fetchall()
    return question_content


def set_question_for_pollid(c, pollid, content):
    sql = """
        REPLACE INTO questions (pollid, content)
        VALUES (?, ?)
    """
    c.execute(sql, (pollid, content))


def set_options_for_pollid(c, pollid, options):
    sql1 = """
        DELETE from options WHERE pollid = ?
    """
    c.execute(sql1, (pollid,))

    for i in range(len(options)):
        sql2 = """
            INSERT into options(pollid, optname) VALUES (?, ?) """
        c.execute(sql2, (pollid, options[i]))


def get_options_for_pollid(c, pollid):
    sql = """
        SELECT * FROM options WHERE pollid = ?
    """
    cur = c.cursor()
    cur.execute(sql, (pollid,))
    rows = cur.fetchall()
    return rows


def create_votes_table(c):
    sql = """
        CREATE TABLE IF NOT EXISTS votes (
            name varchar(225) NOT NULL,
            votes integer NOT NULL Default 0
        );
    """
    c.execute(sql)


def inc_vote(c, pollid, optname):
    sql1 = """
        INSERT OR IGNORE INTO votes (name, votes) VALUES(?, ?)
    """
    c.execute(sql1, (pollid + ":" + optname, 0))

    sql2 = """
        UPDATE votes
            SET votes = votes+1
            WHERE name = ?
    """
    c.execute(sql2, (pollid + ":" + optname,))


def get_votes(c, pollid, optname):
    sql = """
        SELECT votes FROM votes WHERE name = ? LIMIT 1
    """
    cur = c.cursor()
    cur.execute(sql, (pollid + ":" + optname,))
    row = cur.fetchall()
    if len(row) <= 0:
        return 0
    return row[0]["votes"]


def main():
    database = "./pythonsqlite.db"
    conn = create_connection(database)
    create_questions_table(conn)
    create_options_table(conn)
    create_votes_table(conn)
    print("Connection established!")


if __name__ == "__main__":
    main()
