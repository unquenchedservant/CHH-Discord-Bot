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

def set_welcome_channel(channel_id, server_id):
    conn = sqlite3.connect("chh.db")
    updated = False
    try:
        conn.execute("UPDATE server SET welcome_id={} WHERE ID={}".format(channel_id, server_id))
        conn.commit()
        updated = True
    except:
        conn.execute("ALTER TABLE server ADD COLUMN welcome_id int")
        conn.commit()
        conn.execute("UPDATE server SET welcome_id={} WHERE ID={}".format(channel_id, server_id))
        conn.commit()
        updated = False
    return updated

def get_welcome_msg_id(server_id):
    conn = sqlite3.connect("chh.db")
    updated = False
    try:
        cursor = conn.execute("SELECT welcome_msg_id FROM server WHERE ID={}".format(server_id))
        updated=True
    except:
        conn.execute("ALTER TABLE server ADD COLUMN welcome_msg_id int")
        conn.commit()
        cursor = conn.execute("SELECT welcome_msg_id FROM server WHERE ID={}".format(server_id))
    data = cursor.fetchall()
    if len(data) > 0:
        return data[0][0]
    else:
        return False

def get_welcome_channel_id(server_id):
    conn = sqlite3.connect("chh.db")
    updated = False
    try:
        cursor = conn.execute("SELECT welcome_id FROM server WHERE ID={}".format(server_id))
        updated = True
    except:
        conn.execute("ALTER TABLE server ADD COLUMN welcome_id int")
        conn.commit()
        cursor = conn.execute("SELECT welcome_id FROM server WHERE ID={}".format(server_id))
    data = cursor.fetchall()
    if len(data) > 0:
        return data[0][0]
    else:
        return False

def set_welcome_msg_id(msg_id, server_id):
    conn = sqlite3.connect("chh.db")
    conn.execute("UPDATE server SET welcome_msg_id={} WHERE ID={}".format(msg_id, server_id))
    conn.commit()

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

def get_suggestion_channels():
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS allowed
                    (ID INT PRIMARY KEY NOT NULL)''')
    conn.commit()
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

def add_reaction_message(message_id, second_msg_id, user_id, search_string, search_type):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS reactions
                   (ID INT PRIMARY KEY NOT NULL,
                   SECONDMSG INT NOT NULL,
                   USERID INT NOT NULL,
                   SEARCHNUM INT NOT NULL,
                   SEARCH text NOT NULL,
                   TYPE text NOT NULL)''')
    conn.commit()
    conn.execute("INSERT INTO reactions (ID, SECONDMSG, USERID, SEARCH, SEARCHNUM, TYPE) VALUES ({}, {}, {}, '{}', 1, '{}')".format(message_id, second_msg_id, user_id, search_string, search_type))
    conn.commit()
    conn.close()

def get_reaction_user_id(message_id):
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT USERID FROM reactions WHERE ID={}".format(message_id))
    data = cursor.fetchall()
    if len(data) > 0:
        conn.close()
        return data[0][0]

def get_reaction_message_id():
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT ID FROM reactions")
    data = cursor.fetchall()
    ids = []
    for row in data:
        ids.append(row[0])
    conn.close()
    return ids

def get_reaction_message(message_id):
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT * FROM reactions WHERE ID={}".format(message_id))
    data = cursor.fetchall()
    if len(data) > 0:
        conn.close()
        return data[0]

def update_reaction_page(message_id, page_num):
    conn = sqlite3.connect("chh.db")
    conn.execute("UPDATE reactions SET SEARCHNUM={} WHERE ID={}".format(page_num, message_id))
    conn.commit()
    conn.close()


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
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS server
                    (ID INT PRIMARY KEY NOT NULL,
                    PREFIX CHAR(2) NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT ID FROM server")
    data = cursor.fetchall()
    if len(data) == 0:
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
    conn.execute('''CREATE TABLE IF NOT EXISTS reactions
                   (ID INT PRIMARY KEY NOT NULL,
                   SECONDMSG INT NOT NULL,
                   USERID INT NOT NULL,
                   SEARCHNUM INT NOT NULL,
                   SEARCH text NOT NULL,
                   TYPE text NOT NULL)''')

    conn.commit()
    conn.close()
