import sqlite3
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