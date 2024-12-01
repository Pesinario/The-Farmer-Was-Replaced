def ultra_dumb_dyno(bones_target):
    WORLD_TILE_COUNT = get_world_size()**2
    while True:
        if num_items(Items.Egg) < WORLD_TILE_COUNT:
            for i in range(WORLD_TILE_COUNT):
                smart_harv(False)
                walk_the_grid()
            if not acquire_seeds(Items.Egg, WORLD_TILE_COUNT):
                print("We're broke! This went terrible!")
        for i in range(WORLD_TILE_COUNT):
            smart_harv(False)
            use_item(Items.Egg)
            walk_the_grid()
        if num_items(Items.Bones) > bones_target:
            break