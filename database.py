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


def create_table(c):
    sql = """ 
        CREATE TABLE IF NOT EXISTS items (
            id integer PRIMARY KEY,
            name varchar(225) NOT NULL,
            votes integer NOT NULL Default 0
        ); 
    """
    c.execute(sql)


def create_item(c, item):
    sql = """ INSERT INTO items(name)
                VALUES (?) """
    c.execute(sql, item)


def update_item(c, item):
    sql = """ UPDATE items
                SET votes = votes+1 
                WHERE name = ? """
    c.execute(sql, item)


def select_all_items(c, name):
    sql = """ SELECT * FROM items """
    c.execute(sql)

    rows = c.fetchall()
    rows.append({"name": name})
    return json.dumps(rows)


def create_session(c, link):  # incomplete still
    pass


def main():
    database = "./pythonsqlite.db"
    conn = create_connection(database)
    create_questions_table(conn)
    print("Connection established!")


if __name__ == "__main__":
    main()
