def carrots_ensure_seeds(carrot_target):
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
        for i in range(WORLD_TILE_COUNT):
            smart_harv(False)
            if get_ground_type() == Grounds.Soil:
                if not plant(Entities.Carrots):
                    plant(Entities.Bush)
            walk_the_grid()
        if num_items(Items.Carrot) > carrot_target:
            break

def carrots_trusting(carrot_target):
    WORLD_TILE_COUNT = get_world_size()**2

    seeds_to_buy = ((carrot_target - num_items(Items.Carrot) + WORLD_TILE_COUNT) // num_unlocked(Unlocks.Carrots)) + 1
    acquire_seeds(Items.Carrot_Seed, seeds_to_buy)

    for i in range(WORLD_TILE_COUNT): # Initial setting up
        smart_harv(False)
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Carrots)
        walk_the_grid()

    while True:
        if num_items(Items.Carrot_Seed) < WORLD_TILE_COUNT:
            print("Seed issue @ carrots_trusting")
            return False
        #if not acquire_seeds(Items.Carrot_Seed, WORLD_TILE_COUNT):
        #    print("Cant afford seeds, why?!?")
        #    return False
        for i in range(WORLD_TILE_COUNT):
            smart_harv()
            plant(Entities.Carrots)
            walk_the_grid()
        if num_items(Items.Carrot) > carrot_target:
            break

carrots_trusting(num_items(Items.Carrot) + 10000)