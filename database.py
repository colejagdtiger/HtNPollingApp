#db setup file

import sqlite3, json
from sqlite3 import Error

def create_connection(database):
    try:
        conn = sqlite3.connect(database, isolation_level=None, check_same_thread = False)
        conn.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))

        return conn
    except Error as e:
        print(e)

def create_table(conn):
    sql = """ 
        CREATE TABLE IF NOT EXISTS items (
            id integer PRIMARY KEY,
            name varchar(225) NOT NULL,
            votes integer NOT NULL Default 0
        ); 
    """
    conn.execute(sql)

def create_item(conn, item):
    sql = ''' INSERT INTO items(name)
                VALUES (?) '''
    conn.execute(sql, [item])

def update_item(conn, sign, item):
    sql = ''' UPDATE items
                SET votes = votes+? 
                WHERE name = ? '''
    conn.execute(sql, [sign, item])

def select_all_items(conn, name):
    sql = ''' SELECT * FROM items '''
    conn.execute(sql)

    rows = conn.fetchall()
    rows.append({'name' : name})
    return json.dumps(rows)

def create_session(conn, link): #incomplete still
    database = "./pythonsqlite.db"
    conn = create_connection(database)
    create_table(conn)
    create_item(conn, "Yes")
    create_item(conn, "No")

def main():
    database = "./pythonsqlite.db"
    conn = create_connection(database)
    create_table(conn)
    create_item(conn, "Yes")
    create_item(conn, "No")
    print("Connection established!")

if __name__ == '__main__':
    main()
