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
    for i in range(9):
        harvest()
        plant(Entities.Bush)
        walk_the_grid()

    while True:
        if num_items(Items.Wood) > wood_target:
            break
        for i in range(9):
            wait_harv()
            plant(Entities.Bush)
            walk_the_grid()



