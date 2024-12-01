def harv_hay_dumb(hay_target):
    for i in range(get_world_size()):
        harvest()
        if get_ground_type() == Grounds.Soil:
            till()
        move(North)

    while num_items(Items.Hay) < hay_target:
        smart_harv()
        move(North)

def one_by_three_bush(wood_target):
    CONST_GRASS_WAITING = 7
    # initial setup:
    harvest()
    plant(Entities.Bush)
    move(South)
    harvest()
    plant(Entities.Bush)
    move(South)

    while True:
        if num_items(Items.Wood) > wood_target:
            break
        replant = get_entity_type()
        if replant == Entities.Grass:
            for i in range(CONST_GRASS_WAITING):
                wait_harv()
        elif can_harvest():
            harvest()
            plant(Entities.Bush)
        move(North)

def three_by_three_bush(wood_target):
    # initial setup:
    for next_move in precalc:
        harvest()
        plant(Entities.Bush)
        move(next_move)

    while True:
        if num_items(Items.Wood) > wood_target:
            break
        for next_move in precalc:
            wait_harv()
            plant(Entities.Bush)
            move(next_move)

while True:
    print("This file should never be run by itself")
