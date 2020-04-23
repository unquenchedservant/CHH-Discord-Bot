import sqlite3, os


def add_channels(channel_id):
    if not os.path.exists("chh.db"):
        create_table()
    conn = sqlite3.connect("chh.db")
    conn.execute("INSERT INTO allowed (ID) VALUES ({})".format(channel_id))
    conn.commit()
    conn.close()

def remove_channel(channel_id):
    conn = sqlite3.connect("chh.db")
    conn.execute("DELETE FROM allowed WHERE ID = {}".format(channel_id))
    conn.commit()
    conn.close()
def get_allowed_channels():
    if not os.path.exists("chh.db"):
        create_table()
        return []
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT * FROM allowed").fetchall()
    ids = []
    for row in cursor:
        ids.append(row[0])
    conn.close()
    return ids

def add_server(server_id, prefix):
    conn = sqlite3.connect("chh.db")
    conn.execute("INSERT INTO server (ID, PREFIX) VALUES ({}, '{}')".format(server_id, prefix))
    conn.commit()
    conn.close()

def get_prefix(server_id):
    if not os.path.exists("chh.db"):
        create_table()
        add_server(server_id, "&")
        return "&"
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT prefix FROM server WHERE ID = {}".format(server_id))
    data = cursor.fetchall()
    return data[0][0]

def set_prefix(server_id, prefix):
    conn = sqlite3.connect("chh.db")
    conn.execute("UPDATE server SET prefix = '{}' WHERE ID = {}".format(prefix, server_id))
    conn.commit()
    conn.close()

def create_table():
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS server
                    (ID INT PRIMARY KEY NOT NULL,
                    PREFIX CHAR(2) NOT NULL)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
    conn.close()
