def check_month(month):
    if month > 0:
        return month
    else:
        mapping = {
            0: 12,
            -1: 11,
            -2: 10,
            -3: 9,
            -4: 8,
            -5: 7,
            -6: 6,
            -7: 5,
            -8: 4,
            13: 1,
            14: 2,
            15: 3,
            16: 4,
            17: 5,
            18: 6
        }
        return mapping.get(month, None)
    
class Config:
    _instance = None 
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self, is_dev=False):
        self.DEV_ARCH_LVL_1_ID = 745644736341344276
        self.DEV_ARCH_LVL_2_ID = 1383647619448045659

        self.CHH_ARCH_LVL_1_ID = 615702601354182706
        self.CHH_ARCH_LVL_2_ID = 845039809402634240
            
        self.DEV_GUILD_ID = 365879579887534080
        self.CHH_GUILD_ID = 613464665661636648

        self.MODBOARD_DEV_ID = 1366483066494914634
        self.MODBOARD_CHH_ID = 1366482618140459170

        self.STARBOARD_DEV_ID = 1347392583050985612
        self.STARBOARD_CHH_ID = 786775284484669460

        self.SLFPRMO_DEV_ID = 1342566509524029450
        self.SLFPRMO_CHH_ID = 705272855159635969

        self.ROLEMENU_DEV_ID = 1342571477865730089
        self.ROLEMENU_CHH_ID = 975067933673914388

        self.RULES_DEV_ID = 1342581100123258952
        self.RULES_CHH_ID = 844989137551228978

        self.REPORT_DEV_ID = 957645821531258930
        self.REPORT_CHH_ID = 705532389744705616

        self.WELCOME_CHANNEL_ID = 613468039010320415
        self.ARTIST_ROLE_MENU_CHANNEL_ID = 616100468526940195
        self.PARTNERS_CHANNEL_ID = 797240025653051402
        self.MOD_LOG_CHANNEL_ID = 705478973651419167
        self.BOT_COMMANDS_CHANNEL_ID = 702927203360571483
        self.STAFF_HELP_CHANNEL_ID = 909151861892866158
        self.STAFF_CHANNEL_ID = 705463143882686564
        self.STAFF_BOT_CHANNEL_ID = 685566940122447887
        self.STAFF_PARTNER_CHANNEL_ID = 832352549164154900
        self.REDDIT_CHANNEL_ID = 700486332979609671
        self.OWNER_ID = 236394260553924608
        if not hasattr(self, "_initialized"):
            self.is_dev = is_dev
            self._initialized = True
    
    def get_announcements_channel_id(self):
        return 471397293229342781 if self.is_dev else 613469111682334762

    def get_archive_1_id(self):
        return self.DEV_ARCH_LVL_1_ID if self.is_dev else self.CHH_ARCH_LVL_1_ID

    def get_archive_2_id(self):
        return self.DEV_ARCH_LVL_2_ID if self.is_dev else self.CHH_ARCH_LVL_2_ID

    def get_guild_ids(self):
        return [self.DEV_GUILD_ID] if self.is_dev else [self.CHH_GUILD_ID, self.DEV_GUILD_ID]

    def get_guild_id(self):
        return self.DEV_GUILD_ID if self.is_dev else self.CHH_GUILD_ID

    def get_starboard_channel(self):
        return self.STARBOARD_DEV_ID if self.is_dev else self.STARBOARD_CHH_ID
        
    def get_modboard_channel(self):
        return self.MODBOARD_DEV_ID if self.is_dev else self.MODBOARD_CHH_ID

    def get_self_promo_id(self):
        return self.SLFPRMO_DEV_ID if self.is_dev else self.SLFPRMO_CHH_ID

    def get_role_menu_id(self):
        return self.ROLEMENU_DEV_ID if self.is_dev else self.ROLEMENU_CHH_ID

    def get_rules_id(self):
        return self.RULES_DEV_ID if self.is_dev else self.RULES_CHH_ID

    def get_admin_id(self):
        return self.REPORT_DEV_ID if self.is_dev else self.REPORT_CHH_ID
    
    def get_report_id(self):
        return self.REPORT_DEV_ID if self.is_dev else self.REPORT_CHH_ID
    
    def get_staff_help_id(self):
        return self.STAFF_HELP_CHANNEL_ID
    
    def get_welcome_id(self):
        return self.WELCOME_CHANNEL_ID
    
    def get_artist_role_menu_id(self):
        return self.ARTIST_ROLE_MENU_CHANNEL_ID
    
    def get_partners_id(self):
        return self.PARTNERS_CHANNEL_ID
    
    def get_mod_log_id(self):
        return self.MOD_LOG_CHANNEL_ID
    
    def get_bot_commands_id(self):
        return self.BOT_COMMANDS_CHANNEL_ID
    
    def get_staff_id(self):
        return self.STAFF_CHANNEL_ID
    
    def get_staff_bot_id(self):
        return self.STAFF_BOT_CHANNEL_ID
    
    def get_staff_partner_id(self):
        return self.STAFF_PARTNER_CHANNEL_ID
    
    def get_reddit_channel_id(self):
        return self.REDDIT_CHANNEL_ID
    
    def get_owner_id(self):
        return self.OWNER_ID

def zero_leading(number):
    if number < 10:
        return "0{}".format(number)
    else:
        return number