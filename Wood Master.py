def tree_and_bush(wood_target):
    while True:
        for next_move in precalc:
            posSum = get_pos_x()+get_pos_y()
            if posSum % 2 == 0:
                smart_harv(True)
                plant(Entities.Tree)
            else:
                smart_harv(False)
                plant(Entities.Bush)
            move(next_move)
        if num_items(Items.Wood) > wood_target:
            break

# if you wish to run this standalone instead of via timed_run.py, remove the "# "
# precalc = precalc_world()
# tree_and_bush(num_items(Items.Wood) + 10000)