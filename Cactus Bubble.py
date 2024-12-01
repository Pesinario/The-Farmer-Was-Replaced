def do_1_pass_sort(dir_fw, dir_bw):
    # TODO: this can be optimized by remembering whether or not we had to sort 
    # at a certain spot(therefore diminishing the wasted travel over sorted tiles)
    did_swaps = 0
    for i in range(get_world_size()):
        if measure() > measure(dir_fw):
            swap(dir_fw)
            did_swaps += 1
            #print("swapped forwards")
        if measure() < measure(dir_bw):
            swap(dir_bw)
            did_swaps += 1
            #print ("swapped backwards")
        move(dir_fw)
    return did_swaps

def check_work():
    for i in range(get_world_size()**2):
        if get_pos_x() != 0 and get_pos_y() != 0:
            if get_pos_x() != get_world_size()-1 and get_pos_y() != get_world_size()-1:
                if measure() > measure(North) or measure() > measure(East):
                    print("ERROR!!!")
        walk_the_grid()

def cactus_bubble(cactus_target):
    WORLD_TILE_COUNT = get_world_size()**2
    navigate_to(0,0) # this we need for the dumb navigation in the sorting to work
    expected_yield = num_unlocked(Unlocks.Cactus) * get_world_size()**2 * get_world_size()
    for_goal = (cactus_target / expected_yield) * WORLD_TILE_COUNT
    acquire_seeds(Items.Cactus_Seed, for_goal)
    multi_run = False
    for i in range(WORLD_TILE_COUNT):
        harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Cactus)
        walk_the_grid()

    while True: # Main script loop
        # plant the cactus
        if num_items(Items.Cactus_Seed) < WORLD_TILE_COUNT:
            acquire_seeds(Items.Cactus_Seed, WORLD_TILE_COUNT)
        if multi_run:
            for i in range(WORLD_TILE_COUNT):
                plant(Entities.Cactus)
                walk_the_grid()
        else:
            multi_run = True

        # sort the rows
        for x in range(get_world_size()):
            while True:
                debug_var =do_1_pass_sort(East, West)
                if debug_var < 3:
                    break
            move(North)
        
        # sort the columns
        for y in range(get_world_size()):
            while True:
                if do_1_pass_sort(North, South) < 3:
                    break
            move(East)
        
        # print("Done sorting, i think")
        # check_work() this has been disabled cuz it worked
        old_cactus = num_items(Items.Cactus)
        harvest()
        new_cactus = num_items(Items.Cactus)
        actual_yield = new_cactus - old_cactus
        if actual_yield != expected_yield:
            print("Expected yield was: ", expected_yield, " cactus")
            print("We have farmed ", actual_yield, " cactus.")
            print("We farmed ", expected_yield - actual_yield, " less cactus than expected")
            break
        
        if num_items(Items.Cactus) > cactus_target:
            break

cactus_bubble(num_items(Items.Cactus) + 10000)