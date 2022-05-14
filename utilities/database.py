import sqlite3

#role memory functions
def checkRoleMemory(guildid):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS roleMemoryEnabled
                    (GUILDID INT NOT NULL,
                    ENABLED INT NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID={}".format(guildid))
    data = cursor.fetchall()
    status = 1
    if not len(data) == 0:
        return data[0][1]
    else:
        return 0
        
def toggleRoleMemory(guildid):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS roleMemoryEnabled
                    (GUILDID INT NOT NULL,
                    ENABLED INT NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID={}".format(guildid))
    data = cursor.fetchall()
    newEnabled = 1
    if not len(data) == 0:
        if data[0][1] == 0:
            newEnabled = 1
        if data[0][1] == 1:
            newEnabled = 0
        conn.execute("UPDATE roleMemoryEnabled SET ENABLED={} WHERE GUILDID={}".format(newEnabled, guildid))
        conn.commit()
    else:
        conn.execute("INSERT INTO roleMemoryEnabled (GUILDID, ENABLED) VALUES ({},{})".format(guildid, 1))
        conn.commit()
    conn.close()

def getRoleMemoryState(guildid):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS roleMemoryEnabled
                    (GUILDID INT NOT NULL,
                    ENABLED INT NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID={}".format(guildid))
    data = cursor.fetchall()
    if len(data) == 0:
        return False
    else:
        if data[0][1] == 1:
            return True
        else:
            return False

def addRole(uid, rid):
    #uid = user id
    #rid = role id
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS roles
                    (UID INT NOT NULL,
                    RID INT NOT NULL)''')
    conn.commit()
    conn.execute("INSERT INTO roles (UID, RID) VALUES ({},{})".format(uid, rid))
    conn.commit()
    conn.close()

def removeRoles(uid):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS roles
                    (UID INT NOT NULL,
                    RID INT NOT NULL)''')
    conn.commit()
    conn.execute('''DELETE FROM roles WHERE UID={}'''.format(uid))
    conn.commit()
    conn.close()

def getRoles(uid):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS roles
                    (UID INT NOT NULL,
                    RID INT NOT NULL)''')
    cursor = conn.execute("SELECT * FROM roles WHERE UID={}".format(uid))
    data = cursor.fetchall()
    conn.close()
    roles = []
    for item in data:
        roles.append(item[1])
    return roles

#report based functions
def lookUpGuildReport(guildid):
    conn = sqlite3.connect("chh.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS reportchannel
                (GUILDID INT NOT NULL,
                CHANNELID INT NOT NULL)''')
    conn.commit()
    cursor = conn.execute("SELECT * FROM reportchannel WHERE GUILDID={}".format(guildid))
    data = cursor.fetchall()
    if len(data) == 0:
        conn.close()
        return False
    else:
        conn.close()
        return True
def removeGuildReport(guildid):
    conn = sqlite3.connect("chh.db")
    conn.execute("DELETE FROM reportchannel WHERE GUILDID={}".format(guildid))
    conn.commit()
    conn.close()
def setGuildReport(guildid, channelid):
    conn = sqlite3.connect("chh.db")
    conn.execute("INSERT INTO reportchannel (GUILDID, CHANNELID) VALUES ({},{})".format(guildid, channelid))
    conn.commit()
    conn.close()
def updateGuildReport(guildid, channelid):
    conn = sqlite3.connect("chh.db")
    conn.execute("UPDATE reportchannel SET CHANNELID={} WHERE GUILDID={}".format(channelid, guildid))
    conn.commit()
    conn.close()
def getGuildReport(guildid):
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT CHANNELID FROM reportchannel WHERE GUILDID={}".format(guildid))
    data = cursor.fetchone()
    return data[0]