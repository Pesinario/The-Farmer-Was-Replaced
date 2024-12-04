# The functions here should provide a net gain of more than one resource

def one_by_three_bush_hay_wait(wood_target):
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
            return True
        replant = get_entity_type()
        if replant == Entities.Grass:
            for _ in range(CONST_GRASS_WAITING):
                wait_harv()
        elif can_harvest():
            harvest()
            plant(Entities.Bush)
        move(North)

def poly_farm(priority_as_item, target_amount, exclusive = True):
    # Initial setup:
    WORLD_TILE_COUNT = get_world_size()**2
    item_to_ent = {Items.Hay:Entities.Grass, Items.Carrot:Entities.Carrots,
                   Items.Wood:Entities.Tree} # Only these can be companions.
    priority_as_entity = item_to_ent[priority_as_item]
    companion_requests = {}
    for next_move in precalc:
        if get_ground_type() != Grounds.Soil:
            till()
        plant(priority_as_entity)
        move(next_move)

    while True: # Main loop
        acquire_seeds(Items.Carrot_Seed, WORLD_TILE_COUNT, False)

        for next_move in precalc: # Visit every tile once
            current_pos = (get_pos_x(),get_pos_y())
            if current_pos in companion_requests:
                harvest()
                plant(companion_requests.pop(current_pos))
            else:
                harvest()
                plant(priority_as_entity)

            if get_entity_type() != priority_as_entity and exclusive:
                move(next_move)
                continue
            new_comp = get_companion()
            companion_requests[(new_comp[1], new_comp[2])] = new_comp[0]
            move(next_move)

        if num_items(priority_as_item) > target_amount:
            return True

while True:
    print("° This file should be run from Method Tester.py")
