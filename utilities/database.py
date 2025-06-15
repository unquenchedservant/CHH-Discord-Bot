import sqlite3
from utilities.logging import logger

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("chh.db")

    def execute(self, query, params=()):
        try:
            cursor = self.conn.execute(query, params)
            self.conn.commit()
            return cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            cursor.close()

    def check_len(self, data):
        if len(data) == 0:
            return False
        else:
            return True

    def close(self):
        self.connection.close()

class StarboardDB(Database):
    def __init__(self):
        super().__init__()
        self.create()
    
    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS starboard
                              (MSGID INT NOT NULL,
                               STARBOARDMSGID INT NOT NULL)''')
        
    def add(self, msg_id, starboard_msg_id):
        self.execute("INSERT INTO starboard (MSGID, STARBOARDMSGID) VALUES (?,?)", (msg_id, starboard_msg_id))

    def get(self, msg_id):
        data = self.execute("SELECT STARBOARDMSGID FROM starboard WHERE MSGID=?", (msg_id))
        return data[0][0]
    
    def update(self,msg_id,starboard_msg_id):
        self.execute("UPDATE starboard SET STARBOARDMSGID=? WHERE MSGID=?", (starboard_msg_id, msg_id))

    def check(self,msg_id):
        data = self.execute("SELECT * FROM starboard WHERE MSGID=?", (msg_id))
        return self.check_len(data)
    
    def remove(self,msg_id):
        self.execute("DELETE FROM starboard WHERE MSGID=?", (msg_id))
    
    def drop(self):
        self.execute("DROP TABLE starboard")

class Archival(Database):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS archival
                 (CHANNELID INT NOT NULL,
                 MONTH INT NOT NULL,
                 DAY INT NOT NULL,
                 LEVEL INT NOT NULL)''')
        
    def get(self, month, day):
        data = self.execute("SELECT CHANNELID,LEVEL FROM archival WHERE MONTH=? AND DAY=?", (month,day))
        if len(data) == 0:
            return False
        else:
            return data
        
    def check(self, channel_id):
        data = self.execute("SELECT * FROM archival WHERE CHANNELID={}".format(channel_id))
        return data
    
    def set(self, channel_id, month, day, level):
        self.execute("INSERT INTO archival (CHANNELID,MONTH,DAY,LEVEL) VALUES (?,?,?,?)", (channel_id, month, day,level))

    def update(self, channel_id, level):
        self.execute("UPDATE archival SET LEVEL=? WHERE CHANNELID=?", (channel_id, level))
    
    def remove(self, channel_id):
        self.execute("DELETE FROM archival WHERE CHANNELID=?", (channel_id))
    
    def drop(self):
        self.execute("DROP TABLE archival")

class Modboard(Database):
    def __init__(self):
        super().__init__()
        self.create()
    
    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS modboard
                    (MSGID INT NOT NULL,
                    MODBOARDMSGID INT NOT NULL)''')
        
    def add(self, msg_id, modboard_msg_id):
        self.execute("INSERT INTO modboard (MSGID, MODBOARDMSGID) VALUES (?,?)", (msg_id, modboard_msg_id))
        
    def check(self, msg_id):
        data = self.execute("SELECT * FROM modboard WHERE MSGID=?", (msg_id))
        return self.check_len(data)
    
    def get(self, msg_id):
        data = self.execute("SELECT MODBOARDMSGID FROM modboard WHERE MSGID=?", (msg_id))
        return data[0][0]
    
    def update(self, msg_id, modboard_msg_id):
        self.execute("UPDATE modboard SET MODBOARDMSGID=? WHERE MSGID=?", (modboard_msg_id, msg_id))

    def remove(self, msg_id):
        self.execute("DELETE FROM modboard WHERE MSGID=?", (msg_id))

    def drop(self):
        self.execute("DROP TABLE modboard")

class StarboardSettings(Database):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS starboardsettings
                    (GUILDID INT NOT NULL,
                    STARBOARDCHANNEL INT NOT NULL,
                    STARBOARDTHRESHOLD INT NOT NULL)''')
        
    def add(self, guild_id, starboard_channel, starboard_threshold):
        self.execute("INSERT INTO starboardsettings (GUILDID, STARBOARDCHANNEL, STARBOARDTHRESHOLD) VALUES (?,?,?)", (guild_id, starboard_channel, starboard_threshold))

    def check(self, guild_id):
        data = self.execute("SELECT * FROM starboardsettings WHERE GUILDID=?", (guild_id))
        return self.check_len(data)

    def update_channel(self, guild_id, starboard_channel):
        self.execute("UPDATE starboardsettings SET STARBOARDCHANNEL=? WHERE GUILDID=?", (starboard_channel, guild_id))
    
    def update_threshold(self, guild_id, starboard_threshold):
        self.execute("UPDATE starboardsettings SET STARBOARDTHRESHOLD=? WHERE GUILDID=?", (starboard_threshold, guild_id))

    def get_settings(self, guild_id):
        data = self.execute("SELECT STARBOARDCHANNEL, STARBOARDTHRESHOLD FROM starboardsettings WHERE GUILDID=?", (guild_id))
        return data[0]

    def get_threshold(self, guild_id):
        data = self.execute("SELECT STARBOARDTHRESHOLD FROM starboardsettings WHERE GUILDID=?", guild_id)
        return data[0][0]

    def remove(self, guild_id):
        self.execute("DELETE FROM starboardsettings WHERE GUILDID=?", (guild_id))

    def drop(self):
        self.execute("DROP TABLE starboardsettings")

class SelfPromoMsg(Database):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS selfpromomsg
                    (msgID INT NOT NULL)''')
        
    def add(self, msg_id):
        self.execute("INSERT INTO selfpromomsg (msgID) VALUES (?)", (msg_id))
    
    def check(self, msg_id):
        data = self.execute("SELECT * FROM selfpromomsg WHERE msgID=?", (msg_id))
        return self.check_len(data)

class Holiday(Database):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS holidays
                     (MONTH INT NOT NULL,
                     DAY INT NOT NULL,
                     MSG VARCHAR(2000) NOT NULL)''')
        
    def add(self, month, day, msg):
        data = self.execute("SELECT * FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
        updated = False
        if len(data) == 0:
            sql = "INSERT INTO holidays (MONTH, DAY, MSG) VALUES (?,?,\"?\")"
            params = (month,day,msg)
        else:
            updated = True
            sql = "UPDATE holidays SET MSG='?' WHERE MONTH=? AND DAY=?"
            params = (msg, month, day)
        self.execute(sql, params)
        return updated

    def check(self, month, day):
        data = self.execute("SELECT MSG FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
        if len(data) == 0:
            return 0
        else:
            return data[0][0]

    def check_multi(self):
        return self.execute("SELECT * FROM holidays")

    def remove(self, month, day):
        data = self.execute("SELECT * FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
        if len(data) == 0:
            return 0
        else:
            self.execute("DELETE FROM holidays WHERE MONTH=? AND DAY=?", (month,day))
            return 1

class Birthday(Database):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS birthdays
                    (USERID INT NOT NULL,
                    MONTH INT NOT NULL,
                    DAY INT NOT NULL,
                    ACTIVE INT NOT NULL)''')
    
    def get(self, user_id):
        data = self.execute("SELECT * FROM birthdays WHERE USERID=?", (user_id))
        if len(data) == 0:
            return [0, 0]
        else:
            return [data[0][1], data[0][2]]

    def get_multi(self):
        data = self.execute("SELECT USERID FROM birthdays")
        rpkg = []
        for item in data:
            rpkg.append(item[0])
        return rpkg
    
    def set(self, user_id, month, day):
        data = self.execute("SELECT * FROM birthdays WHERE USERID=?", (user_id))
        if len(data) == 0:
            sql = "INSERT INTO birthdays (USERID, MONTH, DAY, ACTIVE) VALUES (?,?,?,?)"
            params = (user_id, month, day, 1)
        else:
            sql = "UPDATE birthdays SET MONTH=?, DAY=?, ACTIVE=? WHERE USERID=?"
            params = (month, day, user_id, 1) 
        self.execute(sql,params)

    def set_active(self, is_active, user_id):
        if is_active:
            isactive_int = 1
        else:
            isactive_int = 0
        self.execute("UPDATE birthdays SET ACTIVE=? WHERE USERID=?", (isactive_int, user_id))

    def check(self, month, day):
        data = self.execute("SELECT USERID, ACTIVE FROM birthdays WHERE MONTH=? AND DAY=?", (month, day))
        if len(data) == 0:
            return []
        else:
            birthday_ids = []
            for item in data:
                if item[1] == 1 or item[1] == None:
                    birthday_ids.append(item[0])
            return birthday_ids

    def remove(self, user_id):
        self.execute("DELETE FROM birthdays WHERE USERID=?", (user_id))

class RoleMemory(Database):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS roleMemoryEnabled
                    (GUILDID INT NOT NULL,
                    ENABLED INT NOT NULL)''')
        
    def check(self, guild_id):
        data = self.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID=?", (guild_id))
        if not len(data) == 0:
            return data[0][1]
        else:
            return 0

    def toggle(self, guild_id):
        data = self.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID=?", (guild_id))
        newEnabled = 1
        if not len(data) == 0:
            if data[0][1] == 0:
                newEnabled = 1
            if data[0][1] == 1:
                newEnabled = 0
            self.execute("UPDATE roleMemoryEnabled SET ENABLED=? WHERE GUILDID=?", (newEnabled, guild_id))
        else:
            self.execute("INSERT INTO roleMemoryEnabled (GUILDID, ENABLED) VALUES (?,?)", (guild_id, 1))

    def get(self, guild_id):
        data = self.execute("SELECT * FROM roleMemoryEnabled WHERE GUILDID=?", (guild_id))
        if len(data) == 0:
            return False
        else:
            if data[0][1] == 1:
                return True
            else:
                return False
            
class Role(Database):
    def __init__(self):
        super().__init__()
        self.create()

    def create(self):
        self.execute('''CREATE TABLE IF NOT EXISTS roles
                    (UID INT NOT NULL,
                    RID INT NOT NULL)''')
        
    def add(self, user_id, role_id):
        self.execute("INSERT INTO roles (UID, RID) VALUES (?,?)", (user_id, role_id))

    def get(self, user_id):
        data = self.execute("SELECT * FROM roles WHERE UID=?", (user_id))
        roles = []
        for item in data:
            roles.append(item[1])
        return roles

    def remove(self, user_id):
        self.execute("DELETE FROM roles WHERE UID=?", (user_id))