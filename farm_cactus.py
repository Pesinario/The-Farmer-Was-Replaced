#"""#This module contains cacti farming methods and their helper functions.#"""#
from navigation import move_helper, navigate_smart, precalc

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

def check_work(): # This is currently not used, but is handy for debugging.
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

def plant_cacti_grouped(length_of_farm):

    def plant_three_lines(dir_fw, dir_left, dir_right):
        for _ in range(get_world_size()):
            plant(Entities.Cactus)
            swap(dir_left)
            plant(Entities.Cactus)
            swap(dir_right)
            plant(Entities.Cactus)
            move(dir_fw)

    def plant_single_line(dir_fw):
        for _ in range(get_world_size()):
            plant(Entities.Cactus)
            move(dir_fw)

    my_y = 0
    while my_y < length_of_farm: # up to y = 9 in 10x10
        if my_y < length_of_farm - 3: # up to y = 7 in 10x10
            move(North) # Place us in the middle
            plant_three_lines(East, North, South)
            move(North) # Move the the most northern line planted
            move(North) # Move to non-planted line
            my_y += 3
        else:
            plant_single_line(East)
            move(North)
            my_y += 1

def ensure_cactus_seeds():
    if num_items(Items.Cactus_Seed) < get_world_size()**2:
        if not trade(Items.Cactus_Seed,
                        get_world_size()**2 - num_items(Items.Cactus_Seed)):
            print("° seed issue @ cactus_bubble")
            return False
    return True

def cactus_bubble(cactus_target): # This farming method is deprecated,
    # as cactus_shaker() is faster by an amazing 2%!, I know, crazy.
    length_of_farm = get_world_size()
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

    is_first = True
    while True: # Main script loop
        navigate_smart([0, 0])
        if not ensure_cactus_seeds():
            return False
        if is_first: # We can't assume the ground is tilled.
            till_and_plant_cacti()
            is_first = False
        else: # Now that we can assume the ground to be tilled, we can go
            # (potentially) faster, not sure if it's actually faster or not
            plant_cacti_grouped(length_of_farm)

        # sort the rows
        for x in range(length_of_farm): # pylint: disable=[W0612]
            while True:
                if bubble_sort_one_line(West, East) < 3: # Two of the "swaps"
                    break # are ghost swaps from being at the edge of the farm.
            move(North)

        # sort the columns
        for y in range(length_of_farm): # pylint: disable=[W0612]
            while True:
                if bubble_sort_one_line(South, North) < 3: # Two of the "swaps" are
                    break # ghost swaps from being at the edge of the farm.
            move(East)

        if not results_expected():
            return False
        if num_items(Items.Cactus) > cactus_target:
            return True


def cactus_shaker(cactus_target):
    length_of_farm = get_world_size()

    # Nested function for better readability
    def martini(dir_bw, dir_fw): # Get it? It's cocktail sort!
        my_index = 1 # Assume we start at index 1 of the field
        last_tile = length_of_farm - 1
        # not_sorted = set(x for x in range(1, last_tile))
        # The game won't let me use generators :(
        not_sorted = set()
        for i in range(my_index, last_tile):
            not_sorted.add(i)

        # Nested function inside a nested function!
        def sorted_from_here(sfh_index):
            here_measured = measure()
            mini_did = True
            did_something = False
            while mini_did:
                mini_did = False
                if here_measured > measure(dir_fw):
                    swap(dir_fw)
                    not_sorted.add(sfh_index) # maybe this can be removed
                    not_sorted.add(sfh_index + 1)
                    did_something = True
                    mini_did = True

                if here_measured < measure(dir_bw):
                    swap(dir_bw)
                    not_sorted.add(sfh_index) # maybe this can be removed
                    not_sorted.add(sfh_index - 1)
                    did_something = True
                    mini_did = True
            return did_something

        # Nested function inside a nested function!
        def pass_forwards(pf_index):
            while True:
                if not sorted_from_here(pf_index):
                    if pf_index in not_sorted:
                        not_sorted.remove(pf_index)
                if pf_index == last_tile - 1:
                    return pf_index
                elif pf_index + 1 not in not_sorted:
                    return pf_index
                else:
                    move(dir_fw)
                    pf_index += 1
        # Private function inside a private function:
        def pass_backwards(pb_index):
            while True:
                if not sorted_from_here(pb_index):
                    if pb_index in not_sorted:
                        not_sorted.remove(pb_index)

                if pb_index == 1:
                    return pb_index
                elif pb_index - 1 not in not_sorted:
                    return pb_index
                else:
                    move(dir_bw)
                    pb_index -= 1

        last_was_forward = True
        while len(not_sorted) > 0:
            offset = 0
            get_me_out = False
            if last_was_forward:
                while my_index - offset not in not_sorted:
                    offset += 1
                    if my_index - offset <= 0:
                        get_me_out = True
                        break
                if get_me_out:
                    last_was_forward = False
                    continue
                else:
                    move_helper(dir_bw, offset)
                    my_index -= offset
                my_index = pass_backwards(my_index)
                last_was_forward = False
            else:
                while my_index + offset not in not_sorted:
                    offset += 1
                    if my_index + offset >= last_tile:
                        get_me_out = True
                        break
                if get_me_out:
                    last_was_forward = True
                    continue
                else:
                    move_helper(dir_fw, offset)
                    my_index += offset
                my_index = pass_forwards(my_index)
                last_was_forward = True

            if 0 in not_sorted:
                not_sorted.remove(0) # We never want to go to 0
            if last_tile in not_sorted:
                not_sorted.remove(last_tile) # We never want to go to the edge

    is_first = True
    while True: # Main script loop
        navigate_smart([0, 0])
        if not ensure_cactus_seeds():
            return False
        if is_first: # We can't assume the ground is tilled.
            till_and_plant_cacti()
            is_first = False
        else: # Now that we can assume the ground to be tilled, we can go
            # (potentially) faster, not sure if it's actually faster or not
            plant_cacti_grouped(length_of_farm)

        for row_number in range(length_of_farm):
            navigate_smart([1, row_number])
            martini(West, East)

        for column_number in range(length_of_farm):
            navigate_smart([column_number, 1])
            martini(South, North)

        if not results_expected():
            return False
        if num_items(Items.Cactus) > cactus_target:
            return True

while True:
    print("° This file should be run from Method Tester.py")
