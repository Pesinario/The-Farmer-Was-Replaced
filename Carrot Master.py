def carrots_ensure_seeds(carrot_target, precalc):
    WORLD_TILE_COUNT = get_world_size()**2
    hay_tiles_per_carrot_tile = get_cost(Items.Carrot_Seed)[Items.Hay] / (num_unlocked(Unlocks.Grass) + 1)
    is_tilled = (WORLD_TILE_COUNT / (1 + hay_tiles_per_carrot_tile) // 1) # Thanks chatGPT for the help with the math lol
    
    till_this_many_tiles(is_tilled, False)
    not_tilled = WORLD_TILE_COUNT - is_tilled
    for i in range(not_tilled):
        harvest()
        if get_ground_type() == Grounds.Soil:
            till()
        walk_the_grid()
    while True:
        trade(Items.Carrot_Seed, is_tilled) # we do NOT use acquire_seeds() because this farming method should farm it's own wood and hay
        for next_move in precalc:
            smart_harv(False)
            if get_ground_type() == Grounds.Soil:
                if not plant(Entities.Carrots):
                    plant(Entities.Bush)
            move(next_move)
        if num_items(Items.Carrot) > carrot_target:
            break

def carrots_trusting(carrot_target, precalc):
    WORLD_TILE_COUNT = get_world_size()**2

    seeds_to_buy = ((carrot_target - num_items(Items.Carrot)) // num_unlocked(Unlocks.Carrots) + WORLD_TILE_COUNT)
    # I got some scary errors trying to split the variable definition
    # This should buy enough seeds to reach our intended amount of carrots, plus a full farmland's worth
    acquire_seeds(Items.Carrot_Seed, seeds_to_buy, precalc)

    for next_move in precalc: # Initial setting up
        smart_harv(False)
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Carrots)
        move(next_move)

    while True:
        if num_items(Items.Carrot_Seed) < WORLD_TILE_COUNT:
            print("Seed issue @ carrots_trusting")
            return False
        for next_move in precalc:
            smart_harv()
            plant(Entities.Carrots)
            move(next_move)
        if num_items(Items.Carrot) > carrot_target:
            break

carrots_trusting(num_items(Items.Carrot) + 10000, precalc_world())