# """#Module that contains functions related to navigation.#"""#

def walk_the_grid():  # This is deprecated but is still used by some also
    # deprecated farming methods.
    if get_pos_y() != get_world_size() - 1:
        move(North)
    else:
        move(North)
        move(East)


def move_helper(direction, duration):
    for _ in range(duration):
        move(direction)


def navigate_dumb(target_x, target_y):  # This has no wrapping but also doesn't use lists
    must_x = target_x - get_pos_x()
    must_y = target_y - get_pos_y()
    if must_x > 0:
        move_helper(East, must_x)
    else:
        move_helper(West, must_x * -1)
    if must_y > 0:
        move_helper(North, must_y)
    else:
        move_helper(South, must_y * -1)


def return_moves_1d(me, target):
    # This should return negative for west/south and positive for north/east
    bound = get_world_size()
    no_wrap = target - me
    if me > target:  # if i'm more east/north than target is
        wrap = bound - me + target
        if wrap < abs(no_wrap):
            return wrap
    else:
        wrap = me + bound - target
        if wrap < abs(no_wrap):
            return wrap * -1

    return no_wrap


def return_closest_target(array_of_targets):
    # TODO: check if this works and then implement it
    current_closest = array_of_targets[0]
    for target in array_of_targets:
        target.insert(
            2,
            abs(return_moves_1d(get_pos_x(), target[0])) +
            abs(return_moves_1d(get_pos_y(), target[1]))
        )
        if current_closest[2] > target[2]:
            current_closest = target
    return current_closest


def navigate_smart(target):
    moves_x = return_moves_1d(get_pos_x(), target[0])
    if moves_x > 0:
        move_helper(East, moves_x)
    else:
        move_helper(West, moves_x * -1)

    moves_y = return_moves_1d(get_pos_y(), target[1])
    if moves_y > 0:
        move_helper(North, moves_y)
    else:
        move_helper(South, moves_y * -1)


def precalc_world():
    # This can be further sped up by precalculating the precalculations using
    # a list with num_unlocked (Unlocks.Expand), but this solution is clearer.
    moves = []
    size = get_world_size()
    for _ in range(size):
        for _ in range(size - 1):
            moves.append(North)
        moves.append(East)
    return moves


precalc = []

while True:
    print("° This file should never be run by itself")
