def walk_the_grid():
    # print(get_pos_x(), get_pos_y())
    if get_pos_y() != get_world_size()-1:
        move(North)
    else:
        move(North)
        move(East)
        