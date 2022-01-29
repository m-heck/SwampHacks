import math
from fighter import Fighter


def find_distance(obj1, obj2):
    x_displacement = int(obj1.get_x() - obj2.get_x())
    y_displacement = int(obj1.get_y() - obj2.get_y())
    distance = math.sqrt(x_displacement ** 2 + y_displacement ** 2)
    return distance


def find_closest(obj1, obj_list):
    min_dist = find_distance(obj1, obj_list[0])
    closest_obj = obj_list[0]
    for obj in obj_list:
        temp_dist = find_distance(obj1, obj)
        if temp_dist < min_dist:
            min_dist = temp_dist
            closest_obj = obj
    return closest_obj
