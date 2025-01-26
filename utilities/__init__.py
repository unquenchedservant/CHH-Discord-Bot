is_dev = False
def get_guild_ids(dev=False):
    if dev:
        return [365879579887534080]
    else:
        return [613464665661636648, 365879579887534080]
def set_is_dev(dev):
    global is_dev
    is_dev = True

def get_is_dev():
    return is_dev

def zero_leading(number):
    if number < 10:
        return "0{}".format(number)
    else:
        return number