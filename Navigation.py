def navigate_to(x, y):
    # print("Navigating to", x, y)
    # navigate_dumb(x, y)
    navigate_smart([x, y])

def move_helper(direction, duration):
    for i in range(duration):
        move(direction)

def navigate_dumb(target_x,target_y): # This has no wrapping but also doesnt use lists
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
    bound = get_world_size() # i do not know if this makes sense or not
    no_wrap = target - me
    if me > target: # if i'm more east/north than target is
        wrap = bound - me + target
        if wrap < abs(no_wrap):
            return wrap
    else:
        wrap = me + bound - target
        if wrap < abs(no_wrap):
            return wrap * -1
            
    return no_wrap
    print("how did we get here wtf")    

def return_closest_target(array_of_targets): # TODO: check if this works and then implement it for pumpkin or sunflower stuff
    current_closest = array_of_targets[0]
    for target in array_of_targets:
        target.insert(2, abs(return_moves_1d(get_pos_x(), target[0])) + 
            abs(return_moves_1d(get_pos_y(), target[1])))
        if current_closest[2] > target[2]:
            current_closest = target
    return current_closest

def navigate_smart(target): # There was a TODO here but it seems to work just fine.
    moves_x = return_moves_1d(get_pos_x(),target[0])
    if moves_x > 0:
        move_helper(East, moves_x)
    else:
        move_helper(West, moves_x * -1)

    moves_y = return_moves_1d(get_pos_y(),target[1])
    if moves_y > 0:
        move_helper(North, moves_y)
    else:
        move_helper(South, moves_y * -1)

def precalc_world():
    moves = []
    size = get_world_size()
    for i in range(size):
        for j in range(size):
            moves.append(North)
        moves.append(East)
    return moves