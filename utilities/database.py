import sqlite3
from utilities.logging import logger

def execute_query(query, params=()):
    with sqlite3.connect("chh.db") as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        conn.close()
        return cursor.fetchall()
    
def check_len(data):
    if len(data) == 0:
        return False
    else:
        return True
"""
=========
Archival Table
=========
"""
def checkArchivalTable():
    execute_query('''CREATE TABLE IF NOT EXISTS archival
                 (CHANNELID INT NOT NULL,
                 MONTH INT NOT NULL,
                 DAY INT NOT NULL)''')
def removeArchivalTable():
    execute_query("DROP TABLE archival")

def getArchival(month, day):
    checkArchivalTable()
    data = execute_query("SELECT CHANNELID FROM modboard WHERE MONTH=? AND DAY=?", (month,day))
    if len(data) == 0:
        return False
    else:
        return data

def setArchival(channelId,month,day):
    checkArchivalTable()
    execute_query("INSERT INTO archival (CHANNELID,MONTH,DAY) VALUES (?,?,?)", (channelId, month, day))

def removeArchival(channelId):
    checkArchivalTable()
    execute_query("DELETE FROM archival WHERE CHANNELID=?", (channelId))


"""
=========
Modboard Table
=========
"""
def checkModboardTable():
    execute_query('''CREATE TABLE IF NOT EXISTS modboard
                    (MSGID INT NOT NULL,
                    MODBOARDMSGID INT NOT NULL)''')

def removeModboardTable():
    execute_query("DROP TABLE modboard")

def checkModboard(msgID):
    checkModboardTable()
    data = execute_query("SELECT * FROM modboard WHERE MSGID=?", (msgID))
    return check_len(data)

def addModboard(msgId, modboardMsgID):
    checkModboardTable()
    execute_query("INSERT INTO modboard (MSGID, MODBOARDMSGID) VALUES (?,?)", (msgId, modboardMsgID))

def getModboardMessage(msgID):
    checkModboardTable()
    data = execute_query("SELECT MODBOARDMSGID FROM modboard WHERE MSGID=?", (msgID))
    return data[0][0]

def updateModboard(msgID, modboardMsgID):
    checkModboardTable()
    execute_query("UPDATE modboard SET MODBOARDMSGID=? WHERE MSGID=?", (modboardMsgID, msgID))

def removeModboard(msgID):
    checkModboardTable()
    execute_query("DELETE FROM modboard WHERE MSGID=?", (msgID))
"""
=========
Starboard Table
=========
"""

def checkStarboardTable():
    execute_query('''CREATE TABLE IF NOT EXISTS starboard
                    (MSGID INT NOT NULL,
                    STARBOARDMSGID INT NOT NULL)''')
    
def removeStarboardTable():
    execute_query("DROP TABLE starboard")

def addStarboard(msgID, starboardMsgID):
    checkStarboardTable()
    execute_query("INSERT INTO starboard (MSGID, STARBOARDMSGID) VALUES (?,?)", (msgID, starboardMsgID))

def checkStarboard(msgID):
    checkStarboardTable()
    data = execute_query("SELECT * FROM starboard WHERE MSGID=?", (msgID))
    return check_len(data)
    
def getStarboardMessage(msgID):
    checkStarboardTable()
    data = execute_query("SELECT STARBOARDMSGID FROM starboard WHERE MSGID=?", (msgID))
    return data[0][0]

def getStarboardThreshold(guildID):
    checkStarboardSettingsTable()
    data = execute_query("SELECT STARBOARDTHRESHOLD FROM starboardsettings WHERE GUILDID=?", format(guildID))
    return data[0][0]

def updateStarboard(msgID, starboardMsgID):
    checkStarboardTable()
    execute_query("UPDATE starboard SET STARBOARDMSGID=? WHERE MSGID=?", (starboardMsgID, msgID))

def removeStarboard(msgID):
    checkStarboardTable()
    execute_query("DELETE FROM starboard WHERE MSGID=?", (msgID))

"""
=========
Starboard Settings Table
=========
"""
def checkStarboardSettingsTable():
    execute_query('''CREATE TABLE IF NOT EXISTS starboardsettings
                    (GUILDID INT NOT NULL,
                    STARBOARDCHANNEL INT NOT NULL,
                    STARBOARDTHRESHOLD INT NOT NULL)''')

def addStarboardSettings(guildID, starboardChannel, starboardThreshold):
    checkStarboardSettingsTable()
    execute_query("INSERT INTO starboardsettings (GUILDID, STARBOARDCHANNEL, STARBOARDTHRESHOLD) VALUES (?,?,?)", (guildID, starboardChannel, starboardThreshold))

def checkStarboardSettings(guildID):
    checkStarboardSettingsTable()
    data = execute_query("SELECT * FROM starboardsettings WHERE GUILDID=?", (guildID))
    return check_len(data)

def updateStarboardChannel(guildID, starboardChannel):
    checkStarboardSettingsTable()
    execute_query("UPDATE starboardsettings SET STARBOARDCHANNEL=? WHERE GUILDID=?", (starboardChannel, guildID))

def updateStarboardThreshold(guildID, starboardThreshold):
    checkStarboardSettingsTable()
    execute_query("UPDATE starboardsettings SET STARBOARDTHRESHOLD=? WHERE GUILDID=?", (starboardThreshold, guildID))

def getStarboardSettings(guildID):
    checkStarboardSettingsTable()
    data = execute_query("SELECT STARBOARDCHANNEL, STARBOARDTHRESHOLD FROM starboardsettings WHERE GUILDID=?", (guildID))
    return data[0]

def removeStarboardSettings(guildID):
    checkStarboardSettingsTable()
    execute_query("DELETE FROM starboardsettings WHERE GUILDID=?", (guildID))

"""
=========
Self-Promo MSG Table
=========
"""

def checkSelfPromoMsgTable():
    execute_query('''CREATE TABLE IF NOT EXISTS selfpromomsg
                    (msgID INT NOT NULL)''')

def addSelfPromoMsg(msgID):
    checkSelfPromoMsgTable()
    execute_query("INSERT INTO selfpromomsg (msgID) VALUES (?)", (msgID))

def checkSelfPromoMsg(msgID):
    checkSelfPromoMsgTable()
    data = execute_query("SELECT * FROM selfpromomsg WHERE msgID=?", (msgID))
    return check_len(data)
"""
=========
Holiday Table
=========
"""
def checkHolidayTable():
    execute_query('''CREATE TABLE IF NOT EXISTS holidays
                     (MONTH INT NOT NULL,
                     DAY INT NOT NULL,
                     MSG VARCHAR(2000) NOT NULL)''')

def addHoliday(month, day, msg):
    checkHolidayTable()
    data = execute_query("SELECT * FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
    updated = False
    if len(data) == 0:
        sql = "INSERT INTO holidays (MONTH, DAY, MSG) VALUES (?,?,\"?\")"
        params = (month,day,msg)
    else:
        updated = True
        sql = "UPDATE holidays SET MSG='?' WHERE MONTH=? AND DAY=?"
        params = (msg, month, day)
    execute_query(sql, params)
    return updated

def checkHoliday(month,day):
    checkHolidayTable()
    data = execute_query("SELECT MSG FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
    if len(data) == 0:
        return 0
    else:
        return data[0][0]

def checkHolidays():
    checkHolidayTable()
    return execute_query("SELECT * FROM holidays")

def removeHoliday(month,day):
    checkHolidayTable()
    data = execute_query("SELECT * FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
    if len(data) == 0:
        return 0
    else:
        execute_query("DELETE FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
        return 1

"""
=========
Birthday Table
=========
"""
def checkBirthdayTable():
    execute_query('''CREATE TABLE IF NOT EXISTS birthdays
                    (USERID INT NOT NULL,
                    MONTH INT NOT NULL,
                    DAY INT NOT NULL,
                    ACTIVE INT NOT NULL)''')

def getBirthdays():
    checkBirthdayTable()
    data = execute_query("SELECT USERID FROM birthdays")
    rpkg = []
    for item in data:
        rpkg.append(item[0])
    return rpkg

def checkBirthday(current_month, current_day):
    checkBirthdayTable()
    data = execute_query("SELECT USERID, ACTIVE FROM birthdays WHERE MONTH=? AND DAY=?", (current_month, current_day))
    if len(data) == 0:
        return []
    else:
        birthday_ids = []
        for item in data:
            if item[1] == 1 or item[1] == None:
                birthday_ids.append(item[0])
        return birthday_ids

def setBirthdayActive(is_active, user_id):
    checkBirthdayTable()
    if is_active:
        isactive_int = 1
    else:
        isactive_int = 0
    execute_query("UPDATE birthdays SET ACTIVE=? WHERE USERID=?", (isactive_int, user_id))

def setBirthday(userid, month, day):
    checkBirthdayTable()
    data = execute_query("SELECT * FROM birthdays WHERE USERID=?", (userid))
    if len(data) == 0:
        sql = "INSERT INTO birthdays (USERID, MONTH, DAY, ACTIVE) VALUES (?,?,?,?)"
        params = (userid, month, day, 1)
    else:
        sql = "UPDATE birthdays SET MONTH=?, DAY=?, ACTIVE=? WHERE USERID=?"
        params = (month, day, userid, 1) 
    execute_query(sql,params)

def removeBirthday(userid):
    checkBirthdayTable()
    execute_query("DELETE FROM birthdays WHERE USERID=?", (userid))

def getBirthday(userid):
    checkBirthdayTable()
    data = execute_query("SELECT * FROM birthdays WHERE USERID=?", (userid))
    if len(data) == 0:
        return [0, 0]
    else:
        return [data[0][1], data[0][2]]

"""
=========
Role Memory Table
=========
"""
def checkRoleMemoryTable():
    execute_query('''CREATE TABLE IF NOT EXISTS roleMemoryEnabled
                    (GUILDID INT NOT NULL,
                    ENABLED INT NOT NULL)''')

def checkRoleMemory(guildid):
    checkRoleMemoryTable()
    data = execute_query("SELECT * FROM roleMemoryEnabled WHERE GUILDID=?", (guildid))
    if not len(data) == 0:
        return data[0][1]
    else:
        return 0
        
def toggleRoleMemory(guildid):
    checkRoleMemoryTable()
    data = execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID=?", (guildid))
    newEnabled = 1
    if not len(data) == 0:
        if data[0][1] == 0:
            newEnabled = 1
        if data[0][1] == 1:
            newEnabled = 0
        execute_query("UPDATE roleMemoryEnabled SET ENABLED=? WHERE GUILDID=?", (newEnabled, guildid))
    else:
        execute_query("INSERT INTO roleMemoryEnabled (GUILDID, ENABLED) VALUES (?,?)", (guildid, 1))

def getRoleMemoryState(guildid):
    checkRoleMemoryTable()
    data = execute_query("SELECT * FROM roleMemoryEnabled WHERE GUILDID=?", (guildid))
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
def checkRoleTable():
    execute_query('''CREATE TABLE IF NOT EXISTS roles
                    (UID INT NOT NULL,
                    RID INT NOT NULL)''')

def addRole(uid, rid):
    checkRoleTable()
    execute_query("INSERT INTO roles (UID, RID) VALUES (?,?)", (uid, rid))

def removeRoles(uid):
    checkRoleTable()
    execute_query("DELETE FROM roles WHERE UID=?", (uid))

def getRoles(uid):
    checkRoleTable()
    data = execute_query("SELECT * FROM roles WHERE UID=?", (uid))
    roles = []
    for item in data:
        roles.append(item[1])
    return roles