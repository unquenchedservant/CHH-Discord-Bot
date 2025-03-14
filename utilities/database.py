import sqlite3
from utilities.logging import logger
"""
=========
Starboard Table
=========
"""

def checkStarboardTable(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS starboard
                    (MSGID INT NOT NULL,
                    STARBOARDMSGID INT NOT NULL)''')
    conn.commit()
    
def removeStarboardTable():
    conn = sqlite3.connect("chh.db")
    conn.execute("DROP TABLE starboard")
    conn.commit()
    conn.close()

def addStarboard(msgID, starboardMsgID):
    conn = sqlite3.connect("chh.db")
    checkStarboardTable(conn)
    sql = "INSERT INTO starboard (MSGID, STARBOARDMSGID) VALUES ({},{})".format(msgID, starboardMsgID)
    conn.execute(sql)
    conn.commit()
    conn.close()

def checkStarboard(msgID):
    conn = sqlite3.connect("chh.db")
    checkStarboardTable(conn)
    cursor = conn.execute("SELECT * FROM starboard WHERE MSGID={}".format(msgID))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return False
    else:
        return True
    
def getStarboardMessage(msgID):
    conn = sqlite3.connect("chh.db")
    checkStarboardTable(conn)
    cursor = conn.execute("SELECT STARBOARDMSGID FROM starboard WHERE MSGID={}".format(msgID))
    data = cursor.fetchall()
    conn.close()
    return data[0][0]

def getStarboardThreshold(guildID):
    conn = sqlite3.connect("chh.db")
    checkStarboardSettingsTable(conn)
    cursor = conn.execute("SELECT STARBOARDTHRESHOLD FROM starboardsettings WHERE GUILDID={}".format(guildID))
    data = cursor.fetchall()
    conn.close()
    return data[0][0]

def updateStarboard(msgID, starboardMsgID):
    conn = sqlite3.connect("chh.db")
    checkStarboardTable(conn)
    conn.execute("UPDATE starboard SET STARBOARDMSGID={} WHERE MSGID={}".format(starboardMsgID, msgID))
    conn.commit()
    conn.close()

def removeStarboard(msgID):
    conn = sqlite3.connect("chh.db")
    checkStarboardTable(conn)
    conn.execute("DELETE FROM starboard WHERE MSGID={}".format(msgID))
    conn.commit()
    conn.close()

"""
=========
Starboard Settings Table
=========
"""
def checkStarboardSettingsTable(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS starboardsettings
                    (GUILDID INT NOT NULL,
                    STARBOARDCHANNEL INT NOT NULL,
                    STARBOARDTHRESHOLD INT NOT NULL)''')
    conn.commit()

def addStarboardSettings(guildID, starboardChannel, starboardThreshold):
    conn = sqlite3.connect("chh.db")
    checkStarboardSettingsTable(conn)
    sql = "INSERT INTO starboardsettings (GUILDID, STARBOARDCHANNEL, STARBOARDTHRESHOLD) VALUES ({},{},{})".format(guildID, starboardChannel, starboardThreshold)
    conn.execute(sql)
    conn.commit()
    conn.close()

def checkStarboardSettings(guildID):
    conn = sqlite3.connect("chh.db")
    checkStarboardSettingsTable(conn)
    cursor = conn.execute("SELECT * FROM starboardsettings WHERE GUILDID={}".format(guildID))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return False
    else:
        return True

def updateStarboardChannel(guildID, starboardChannel):
    conn = sqlite3.connect("chh.db")
    checkStarboardSettingsTable(conn)
    conn.execute("UPDATE starboardsettings SET STARBOARDCHANNEL={} WHERE GUILDID={}".format(starboardChannel, guildID))
    conn.commit()
    conn.close()

def updateStarboardThreshold(guildID, starboardThreshold):
    conn = sqlite3.connect("chh.db")
    checkStarboardSettingsTable(conn)
    conn.execute("UPDATE starboardsettings SET STARBOARDTHRESHOLD={} WHERE GUILDID={}".format(starboardThreshold, guildID))
    conn.commit()
    conn.close()

def getStarboardSettings(guildID):
    conn = sqlite3.connect("chh.db")
    checkStarboardSettingsTable(conn)
    cursor = conn.execute("SELECT STARBOARDCHANNEL, STARBOARDTHRESHOLD FROM starboardsettings WHERE GUILDID={}".format(guildID))
    data = cursor.fetchall()
    conn.close()
    return data[0]

def removeStarboardSettings(guildID):
    conn = sqlite3.connect("chh.db")
    checkStarboardSettingsTable(conn)
    conn.execute("DELETE FROM starboardsettings WHERE GUILDID={}".format(guildID))
    conn.commit()
    conn.close()

"""
=========
Self-Promo MSG Table
=========
"""

def checkSelfPromoMsgTable(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS selfpromomsg
                    (msgID INT NOT NULL)''')
    conn.commit()

def addSelfPromoMsg(msgID):
    conn = sqlite3.connect("chh.db")
    checkSelfPromoMsgTable(conn)
    sql = "INSERT INTO selfpromomsg (msgID) VALUES ({})".format(msgID)
    conn.execute(sql)
    conn.commit()
    conn.close()

def checkSelfPromoMsg(msgID):
    conn = sqlite3.connect("chh.db")
    checkSelfPromoMsgTable(conn)
    cursor = conn.execute("SELECT * FROM selfpromomsg WHERE msgID={}".format(msgID))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return False
    else:
        return True
"""
=========
Holiday Table
=========
"""
def checkHolidayTable(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS holidays
                     (MONTH INT NOT NULL,
                     DAY INT NOT NULL,
                     MSG VARCHAR(2000) NOT NULL)''')
    conn.commit()

def addHoliday(month, day, msg):
    conn = sqlite3.connect("chh.db")
    checkHolidayTable(conn)
    cursor = conn.execute("SELECT * FROM holidays WHERE MONTH={} AND DAY={}".format(month,day))
    data = cursor.fetchall()
    updated = False
    if len(data) == 0:
        sql = "INSERT INTO holidays (MONTH, DAY, MSG) VALUES ({},{},\"{}\")".format(month,day,msg)
    else:
        updated = True
        sql = "UPDATE holidays SET MSG='{}' WHERE MONTH={} AND DAY={}".format(msg, month, day)
    conn.execute(sql)
    conn.commit()
    conn.close()
    return updated

def checkHoliday(month,day):
    conn = sqlite3.connect("chh.db")
    checkHolidayTable(conn)
    cursor = conn.execute("SELECT MSG FROM holidays WHERE MONTH={} AND DAY={}".format(month,day))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return 0
    else:
        return data[0][0]

def checkHolidays():
    conn = sqlite3.connect("chh.db")
    checkHolidayTable(conn)
    cursor = conn.execute("SELECT * FROM holidays")
    data = cursor.fetchall()
    conn.close()
    return data

def removeHoliday(month,day):
    conn =sqlite3.connect("chh.db")
    checkHolidayTable(conn)
    cursor = conn.execute("SELECT * FROM holidays WHERE MONTH={} AND DAY={}".format(month,day))
    data = cursor.fetchall()
    if len(data) == 0:
        conn.close()
        return 0
    else:
        conn.execute("DELETE FROM holidays WHERE MONTH={} AND DAY={}".format(month,day))
        conn.commit()
        conn.close()
        return 1

"""
=========
Birthday Table
=========
"""
def checkBirthdayTable(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS birthdays
                    (USERID INT NOT NULL,
                    MONTH INT NOT NULL,
                    DAY INT NOT NULL,
                    ACTIVE INT NOT NULL)''')
    conn.commit()

def getBirthdays():
    conn = sqlite3.connect("chh.db")
    cursor = conn.execute("SELECT USERID FROM birthdays")
    data = cursor.fetchall()
    rpkg = []
    for item in data:
        rpkg.append(item[0])
    return rpkg

def checkBirthday(current_month, current_day):
    conn = sqlite3.connect("chh.db")
    checkBirthdayTable(conn)
    cursor = conn.execute("SELECT USERID, ACTIVE FROM birthdays WHERE MONTH={} AND DAY={}".format(current_month, current_day))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return []
    else:
        birthday_ids = []
        for item in data:
            if item[1] == 1:
                birthday_ids.append(item[0])
        return birthday_ids

def setBirthdayActive(is_active, user_id):
    conn = sqlite3.connect("chh.db")
    checkBirthdayTable(conn)
    isactive_int = 0
    if is_active:
        isactive_int = 1
    else:
        isactive_int = 0
    conn.execute("UPDATE birthdays SET ACTIVE={} WHERE USERID={}".format(isactive_int, user_id))
    conn.commit()
    conn.close()

def setBirthday(userid, month, day):
    conn = sqlite3.connect("chh.db")
    checkBirthdayTable(conn)
    cursor = conn.execute("SELECT * FROM birthdays WHERE USERID={}".format(userid))
    data = cursor.fetchall()
    if len(data) == 0:
        sql = "INSERT INTO birthdays (USERID, MONTH, DAY, ACTIVE) VALUES ({},{},{},{})".format(userid, month, day, 1)
    else:
        sql = "UPDATE birthdays SET MONTH={}, DAY={}, ACTIVE={} WHERE USERID={}".format(month, day, userid, 1) 
    conn.execute(sql)
    conn.commit()
    conn.close()

def removeBirthday(userid):
    conn = sqlite3.connect("chh.db")
    checkBirthdayTable(conn)
    conn.execute('''DELETE FROM birthdays WHERE USERID={}'''.format(userid))
    conn.commit()
    conn.close()

def getBirthday(userid):
    conn = sqlite3.connect("chh.db")
    checkBirthdayTable(conn)
    cursor = conn.execute ("SELECT * FROM birthdays WHERE USERID={}".format(userid))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return [0, 0]
    else:
        month=data[0][1]
        day=data[0][2]
        return [month, day]

"""
=========
Role Memory Table
=========
"""
def checkRoleMemoryTable(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS roleMemoryEnabled
                    (GUILDID INT NOT NULL,
                    ENABLED INT NOT NULL)''')
    conn.commit()

#role memory functions
def checkRoleMemory(guildid):
    conn = sqlite3.connect("chh.db")
    checkRoleMemoryTable(conn)
    cursor = conn.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID={}".format(guildid))
    data = cursor.fetchall()
    status = 1
    conn.close()
    if not len(data) == 0:
        return data[0][1]
    else:
        return 0
        
def toggleRoleMemory(guildid):
    conn = sqlite3.connect("chh.db")
    checkRoleMemoryTable(conn)
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
    checkRoleMemoryTable(conn)
    cursor = conn.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID={}".format(guildid))
    data = cursor.fetchall()
    conn.close()
    if len(data) == 0:
        return False
    else:
        if data[0][1] == 1:
            return True
        else:
            return False

"""
=========
Role Table
=========
"""
def checkRoleTable(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS roles
                    (UID INT NOT NULL,
                    RID INT NOT NULL)''')
    conn.commit()

def addRole(uid, rid):
    #uid = user id
    #rid = role id
    conn = sqlite3.connect("chh.db")
    checkRoleTable(conn)
    conn.execute("INSERT INTO roles (UID, RID) VALUES ({},{})".format(uid, rid))
    conn.commit()
    conn.close()

def removeRoles(uid):
    conn = sqlite3.connect("chh.db")
    checkRoleTable(conn)
    conn.execute('''DELETE FROM roles WHERE UID={}'''.format(uid))
    conn.commit()
    conn.close()

def getRoles(uid):
    conn = sqlite3.connect("chh.db")
    checkRoleTable(conn)
    cursor = conn.execute("SELECT * FROM roles WHERE UID={}".format(uid))
    data = cursor.fetchall()
    conn.close()
    roles = []
    for item in data:
        roles.append(item[1])
    return roles

#report based functions (I have no idea if these are still used?)
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

def updateDB():
    conn = sqlite3.connect("chh.db")
    conn.execute("ALTER TABLE birthdays ADD COLUMN ACTIVE INT")
    conn.commit()
