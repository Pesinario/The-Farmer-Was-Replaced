def do_1_pass_sort(dir_fw, dir_bw):
    # TODO: this can be optimized by remembering whether or not we had to sort
    # at a certain spot(therefore diminishing the wasted travel over sorted tiles)
    # i think that's known as cocktail sort instead of bubble sort
    did_swaps = 0
    for _ in range(get_world_size()):
        if measure() > measure(dir_fw):
            swap(dir_fw)
            did_swaps += 1
        if measure() < measure(dir_bw):
            swap(dir_bw)
            did_swaps += 1
        move(dir_fw)
    return did_swaps

def check_work(precalc): # This is currently not called because it just works.
    for next_move in precalc:
        if get_pos_x() != 0 and get_pos_y() != 0:
            if get_pos_x() != get_world_size()-1 and get_pos_y() != get_world_size()-1:
                if measure() > measure(North) or measure() > measure(East):
                    print("° ERROR!!!")
        move(next_move)

def cactus_bubble(cactus_target):
    if get_entity_type() == Entities.Hedge or get_entity_type() == Entities.Treasure:
        harvest() # Somehow we get here while in a maze sometimes. probably can fix it elsewhere.
    expected_yield = num_unlocked(Unlocks.Cactus) * get_world_size()**3
    while True: # Main script loop
        navigate_to(0,0) # this we need for the dumb navigation in the sorting to work
        if num_items(Items.Cactus_Seed) < get_world_size()**2:
            print("° seed issue @ cactus_bubble")
            return False
        # plant the cactus:
        for next_move in precalc:
            harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Cactus)
            move(next_move)
        navigate_to(0,0) # this we need for the dumb navigation in the sorting to work
        # sort the rows
        for x in range(get_world_size()): # pylint: disable=[W0612]
            while True:
                debug_var =do_1_pass_sort(East, West)
                if debug_var < 3:
                    break
            move(North)

        # sort the columns
        for y in range(get_world_size()): # pylint: disable=[W0612]
            while True:
                if do_1_pass_sort(North, South) < 3:
                    break
            move(East)

        old_cactus = num_items(Items.Cactus)
        harvest()
        new_cactus = num_items(Items.Cactus)
        actual_yield = new_cactus - old_cactus
        if actual_yield != expected_yield:
            print("° Expected yield was: ", expected_yield, " cactus")
            print("° We have farmed ", actual_yield, " cactus.")
            print("° We farmed ", expected_yield - actual_yield, " less cactus than expected")
            return False

        if num_items(Items.Cactus) > cactus_target:
            return True

while True:
    print("° This file should be run from Method Tester.py")
