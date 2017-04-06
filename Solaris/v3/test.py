

def switch_keys(old_dict):
    new_dict = {}
    for key in old_dict:
        new_dict[old_dict[key]] = key
    return new_dict


if __name__ == '__main__':
    old_dict = {42: 'Marty', 81: 'Sue', 17: 'Ed', 31: 'Dave', 56: 'Ed'}
    new_dict = switch_keys(old_dict)
    print(new_dict)
