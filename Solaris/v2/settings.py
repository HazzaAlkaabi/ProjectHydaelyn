

def init():
    global global_list
    global_list = {}

def get_global(name):
    for thing in global_list:
        if thing == name:
            return global_list[]