import math


def game_pos_to_screen(pos, camera_pos):
    game_pos = [pos[0] - camera_pos[0], pos[1] - camera_pos[1]]
    return game_pos


def get_distance(pos1, pos2):
    distx = abs(pos1[0] - pos2[0])
    disty = abs(pos1[1] - pos2[1])
    dist = math.sqrt((distx**2) + (disty**2))
    return dist


def normalize(vector):
    mag = math.sqrt(vector[0]**2 + vector[1]**2)
    norm = [vector[0]/mag, vector[1]/mag]
    return norm


def round_list(some_list):
    new_list = []
    for item in some_list:
        new_list.append(round(item))
    return new_list
