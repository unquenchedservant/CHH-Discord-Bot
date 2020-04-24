import sqlite3, os

'''
ADD TRACKING UTILITY FUNCTIONS

add_suggestion_channel - adds tracking for suggestions to the given channel_id

add_recommendation_channel - adds tracking for recommendations to the given channel_id
'''

def add_suggestion_channel(channel_id):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM allowed WHERE ID={}".format(channel_id))
    data = cursor.fetchall()
    if len(data) == 0:
        conn.execute("INSERT INTO allowed (ID) VALUES ({})".format(channel_id))
        conn.commit()
        conn.close()
        return True
    else:
        return False

def add_recommendation_channel(channel_id):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed_recommended
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM allowed_recommended WHERE ID={}".format(channel_id))
    data = cursor.fetchall()
    if len(data) == 0:
        conn.execute("INSERT INTO allowed_recommended (ID) VALUES ({})".format(channel_id))
        conn.commit()
        conn.close()
        return True
    else:
        return False


'''
REMOVE TRACKING UTILITY FUNCTIONS

remove_suggestion_channel - removes tracking for suggestions from the channel with given ID

remove_recommendation_channel - removes tracking for recommendations from the channel with given id
'''
def remove_suggestion_channel(channel_id):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM allowed WHERE ID={}".format(channel_id))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        conn.execute("DELETE FROM allowed WHERE ID = {}".format(channel_id))
        conn.commit()
        conn.close()
        return True

def remove_recommendation_channel(channel_id):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed_recommended
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM allowed_recommended WHERE ID={}".format(channel_id))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        conn.execute("DELETE FROM allowed_recommended WHERE ID = {}".format(channel_id))
        conn.commit()
        conn.close()
        return True

def get_allowed_channels():
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT * FROM allowed").fetchall()
    ids = []
    for row in cursor:
        ids.append(row[0])
    conn.close()
    return ids





def get_recommended_channels():
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed_recommended
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM allowed_recommended").fetchall()
    ids = []
    for row in cursor:
        ids.append(row[0])
    conn.close()
    return ids

def add_server(server_id, prefix):
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT ID FROM server")
    data = cursor.fetchall()
    found = False
    for row in data:
        if row[0] == server_id:
            found = True
            break
    if not found:
        conn.execute("INSERT INTO server (ID, PREFIX) VALUES ({}, '{}')".format(server_id, prefix))
        conn.commit()
        conn.close()

def get_prefix(server_id):
    if not os.path.exists("chh.db"):
        create_table()
        add_server(server_id, "^")
        return "^"
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT ID FROM server")
    data = cursor.fetchall()
    if not data[0][0] == server_id:
        add_server(server_id, "^")
    cursor = conn.execute("SELECT prefix FROM server WHERE ID = {}".format(server_id))
    data = cursor.fetchall()
    if len(data) == 0:
        add_server(server_id, "^")
        return "^"
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
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed_recommended
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
    conn.close()
