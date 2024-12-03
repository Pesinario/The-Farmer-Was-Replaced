def harv_hay_dumb(hay_target):
    for i in range(get_world_size()):
        harvest()
        if get_ground_type() != Grounds.Turf:
            till()
        move(North)

    while num_items(Items.Hay) < hay_target:
        if not can_harvest():
            if get_entity_type() == Entities.Grass:
                print("° We outspeed grass! confirmed")
        harvest()
        move(North)
    return True

def hay_full_field(hay_target):
    for next_move in precalc: # Initial setting up
        harvest()
        if get_ground_type() != Grounds.Turf:
            till()
        move(next_move)
    while num_items(Items.Hay) < hay_target:
        for next_move in precalc: # Main loop
            harvest()
            move(next_move)
    return True

while True:
    print("° This file should be run from Method Tester.py")
