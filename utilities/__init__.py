is_dev = False
def get_guild_ids():
    if is_dev:
        return [365879579887534080]
    else:
        return [613464665661636648, 365879579887534080]
    
def get_starboard_channel():
    if is_dev:
        return 1347392583050985612
    else:
        return 786775284484669460
    
def get_self_promo_id():
    if is_dev:
        return 1342566509524029450
    else:
        return 705272855159635969

def get_role_menu_id():
    if is_dev:
        return 1342571477865730089
    else:
        return 975067933673914388

def get_rules_id():
    if is_dev:
        return 1342581100123258952
    else:
        return 844989137551228978

def get_admin_id():
    if is_dev:
        return 957645821531258930
    else:
        return 705532389744705616
def set_is_dev(dev):
    global is_dev
    is_dev = True

def zero_leading(number):
    if number < 10:
        return "0{}".format(number)
    else:
        return number