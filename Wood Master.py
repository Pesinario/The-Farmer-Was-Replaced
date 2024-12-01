def tree_and_bush(wood_target):
    WORLD_TILE_COUNT = get_world_size()**2
    while True:
        for i in range(WORLD_TILE_COUNT):
            posSum = get_pos_x()+get_pos_y()
            if posSum % 2 == 0:
                smart_harv(True)
                plant(Entities.Tree)
            else:
                smart_harv(False)
                plant(Entities.Bush)
            walk_the_grid()
        if num_items(Items.Wood) > wood_target:
            break

tree_and_bush(num_items(Items.Wood) + 10000)