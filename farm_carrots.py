def carrots_ensure_seeds(carrot_target):
    WORLD_TILE_COUNT = get_world_size()**2
    hay_tiles_per_carrot_tile = get_cost(Items.Carrot_Seed)[Items.Hay] / (
        num_unlocked(Unlocks.Grass) + 1)
    is_tilled = WORLD_TILE_COUNT / (1 + hay_tiles_per_carrot_tile) // 1

    till_this_many_tiles(is_tilled, False)
    not_tilled = WORLD_TILE_COUNT - is_tilled
    for _ in range(not_tilled):
        harvest()
        if get_ground_type() == Grounds.Soil:
            till()
        walk_the_grid()
    while True:
        trade(Items.Carrot_Seed, is_tilled) # we do NOT use acquire_seeds()
        # because this farming method should farm its own wood and hay
        for next_move in precalc:
            smart_harv(False)
            if get_ground_type() == Grounds.Soil:
                if not plant(Entities.Carrots):
                    plant(Entities.Bush)
            move(next_move)
        if num_items(Items.Carrot) > carrot_target:
            return True

def carrots_trusting(carrot_target):
    WORLD_TILE_COUNT = get_world_size()**2

    seeds_to_buy = ((carrot_target - num_items(Items.Carrot)) // (
        num_unlocked(Unlocks.Carrots) + WORLD_TILE_COUNT))
    # This should buy enough seeds ahead of time to reach our goal plus
    # a full famrland's worth for safety
    if not acquire_seeds(Items.Carrot_Seed, seeds_to_buy):
        print("° Seed issue at acquire_seeds() -> carrots_trusting(), not my fault boss")
        return False

    for next_move in precalc: # Initial setting up
        smart_harv(False)
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Carrots)
        move(next_move)

    while True: # Main loop
        if num_items(Items.Carrot) > carrot_target:
            return True
        elif num_items(Items.Carrot_Seed) < WORLD_TILE_COUNT:
            print("° Seed issue @ carrots_trusting")
            return False
        for next_move in precalc:
            smart_harv()
            plant(Entities.Carrots)
            move(next_move)

while True:
    print("° This file should be run from Method Tester.py")
