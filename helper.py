import fighter


def step(obj, window, steps, direction):
    if direction == "right":
        obj.move_right()
    elif direction == "left":
        obj.move_left()
    elif direction == "down":
        obj.move_down()
    elif direction == "up":
        obj.move_up()