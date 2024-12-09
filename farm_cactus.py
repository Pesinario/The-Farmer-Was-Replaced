def results_expected():
    expected_yield = num_unlocked(Unlocks.Cactus) * get_world_size()**3
    old_cactus = num_items(Items.Cactus)
    harvest()
    new_cactus = num_items(Items.Cactus)
    actual_yield = new_cactus - old_cactus
    if actual_yield != expected_yield:
        print("° Expected yield was: ", expected_yield, " cactus")
        print("° We have farmed ", actual_yield, " cactus.")
        print("° We farmed ", expected_yield - actual_yield, " less cactus than expected")
        return False
    return True

def check_work(): # This is currently not called because buble sort works 99%
    upper_bound = get_world_size() - 1
    for next_move in precalc:
        cur_measure = measure()
        pos_x = get_pos_x() # I wonder if using `in range()` would be faster or
        pos_y = get_pos_y() # not, certainly would be prettier. TODO: check

        # Check along the X axis, but not if we're on the edges
        if pos_x != 0 and cur_measure < measure(West):
            print("° ERROR during cactus sorting (horizontal)")
            return False
        if pos_x != upper_bound and cur_measure > measure(East):
            print("° ERROR during cactus sorting (horizontal)")
            return False
        # Check along the X axis, but not if we're on the edges
        if pos_y != 0 and cur_measure < measure(South):
            print("° ERROR during cactus sorting (vertical)")
            return False
        if pos_y != upper_bound and cur_measure > measure(North):
            print("° ERROR during cactus sorting (vertical)")
            return False
        # Continue checking
        move(next_move)
    return True

def till_and_plant_cacti():
    for next_move in precalc:
        harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Cactus)
        move(next_move)

def ensure_cactus_seeds():
    if num_items(Items.Cactus_Seed) < get_world_size()**2:
        if not trade(Items.Cactus_Seed,
                        get_world_size()**2 - num_items(Items.Cactus_Seed)):
            print("° seed issue @ cactus_bubble")
            return False
    return True

def cactus_bubble(cactus_target): # This farming method is deprecated, as cactus_shaker() is faster
    def bubble_sort_one_line(dir_bw, dir_fw):
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

    while True: # Main script loop
        if not ensure_cactus_seeds():
            return False
        till_and_plant_cacti()

        # sort the rows
        for x in range(get_world_size()): # pylint: disable=[W0612]
            while True:
                if bubble_sort_one_line(West, East) < 3: # Two of the "swaps"
                    break # are ghost swaps from being at the edge of the farm.
            move(North)

        # sort the columns
        for y in range(get_world_size()): # pylint: disable=[W0612]
            while True:
                if bubble_sort_one_line(South, North) < 3: # Two of the "swaps" are
                    break # ghost swaps from being at the edge of the farm.
            move(East)

        if not results_expected():
            return False
        if num_items(Items.Cactus) > cactus_target:
            return True

while True:
    print("° This file should be run from Method Tester.py")
