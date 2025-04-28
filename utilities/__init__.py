is_dev = False
from utilities.logging import logger



def get_announcements_channel_id():
    if is_dev:
        return 471397293229342781 
    else:
        return 613469111682334762
        
def get_guild_ids():
    if is_dev:
        return [DEV_GUILD_ID]
    else:
        return [CHH_GUILD_ID, DEV_GUILD_ID]
    
def get_guild_id():
    if is_dev:
        return DEV_GUILD_ID
    else:
        return CHH_GUILD_ID
    
def get_starboard_channel():
    if is_dev:
        return STARBOARD_DEV_ID
    else:
        return STARBOARD_CHH_ID
    
def get_modboard_channel():
    if is_dev:
        print("IS DEV")
        return MODBOARD_DEV_ID
    else:
        print("IS NOT DEV")
        return MODBOARD_CHH_ID

def get_self_promo_id():
    if is_dev:
        return SLFPRMO_DEV_ID
    else:
        return SLFPRMO_DEV_ID

def get_role_menu_id():
    if is_dev:
        return ROLEMENU_DEV_ID
    else:
        return ROLEMENU_CHH_ID

def get_rules_id():
    if is_dev:
        return RULES_DEV_ID
    else:
        return RULES_CHH_ID

def get_admin_id():
    if is_dev:
        return REPORT_DEV_ID
    else:
        return REPORT_CHH_ID

DEV_GUILD_ID = 365879579887534080
CHH_GUILD_ID = 613464665661636648

MODBOARD_DEV_ID = 1366483066494914634
MODBOARD_CHH_ID = 1366482618140459170

STARBOARD_DEV_ID = 1347392583050985612
STARBOARD_CHH_ID = 786775284484669460

SLFPRMO_DEV_ID = 1342566509524029450
SLFPRMO_CHH_ID = 705272855159635969

ROLEMENU_DEV_ID = 1342571477865730089
ROLEMENU_CHH_ID = 975067933673914388

RULES_DEV_ID = 1342581100123258952
RULES_CHH_ID = 844989137551228978

REPORT_DEV_ID = 957645821531258930
REPORT_CHH_ID = 705532389744705616

MODBOARD_CHANNEL_ID = get_modboard_channel()
STARBOARD_CHANNEL_ID = get_starboard_channel()
SELF_PROMO_CHANNEL_ID = get_self_promo_id()
GUILD_IDS = get_guild_ids()
GUILD_ID = get_guild_id()
ROLE_MENU_CHANNEL_ID = get_role_menu_id()
RULE_CHANNEL_ID = get_rules_id()
REPORT_CHANNEL_ID = get_admin_id()
WELCOME_CHANNEL_ID = 613468039010320415
ARTIST_ROLE_MENU_CHANNEL_ID = 616100468526940195
PARTNERS_CHANNEL_ID = 797240025653051402
ANNOUNCEMENTS_CHANNEL_ID = get_announcements_channel_id()
MOD_LOG_CHANNEL_ID = 705478973651419167
BOT_COMMANDS_CHANNEL_ID = 702927203360571483
STAFF_HELP_CHANNEL_ID = 909151861892866158
STAFF_CHANNEL_ID = 705463143882686564
STAFF_BOT_CHANNEL_ID = 685566940122447887
STAFF_PARTNER_CHANNEL_ID = 832352549164154900
REDDIT_CHANNEL_ID = 700486332979609671
OWNER_ID = 236394260553924608

class ChannelIds():

    def __init__(self):
        self.updateIds()
        
    def updateIds(self):
        global STARBOARD_CHANNEL_ID
        global MODBOARD_CHANNEL_ID
        global SELF_PROMO_CHANNEL_ID
        global GUILD_IDS
        global GUILD_ID
        global ROLE_MENU_CHANNEL_ID
        global RULE_CHANNEL_ID
        global REPORT_CHANNEL_ID
        global ANNOUNCEMENTS_CHANNEL_ID
        MODBOARD_CHANNEL_ID = get_modboard_channel()
        STARBOARD_CHANNEL_ID = get_starboard_channel()
        SELF_PROMO_CHANNEL_ID = get_self_promo_id()
        GUILD_IDS = get_guild_ids()
        ROLE_MENU_CHANNEL_ID = get_role_menu_id()
        RULE_CHANNEL_ID = get_rules_id()
        REPORT_CHANNEL_ID = get_admin_id()
        ANNOUNCEMENTS_CHANNEL_ID = get_announcements_channel_id()
        GUILD_ID = get_guild_id()
    


def set_is_dev(dev):
    global is_dev
    is_dev = dev
    ChannelIds().updateIds()

def zero_leading(number):
    if number < 10:
        return "0{}".format(number)
    else:
        return number