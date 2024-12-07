# The functions here should provide a net gain of more than one resource

def one_by_three_bush_hay_wait(wood_target):
    def h_p_and_m(direction = South): # Private function
        harvest()
        plant(Entities.Bush)
        move(direction)

    CONST_GRASS_WAITING = 3.5 * (num_unlocked(Unlocks.Speed) + 1)
    # This is not as much wood as possible, but it's close enough while not
    # wasting any time, we'll need hay anyways.
    h_p_and_m() # 0 -> 1
    while True:
        if num_items(Items.Wood) > wood_target:
            for _ in range(3): # Do not waste the bushes, since we're about to buy expand 2
                harvest()
                move(North)
            return True

        h_p_and_m() # 1 -> 2

        for _ in range(CONST_GRASS_WAITING):
            wait_harv()
        plant(Entities.Bush)
        move(South) # 2 -> 0

def three_by_three_with_hay(wood_target):
    # this takes 73.56 seconds compared to the 61.22 seconds from three_by_three_bush()
    # to farm the 100 wood that it costs to get carrots, but it also gets 28 more hay
    # in exchange for taking ~20% longer
    def h_p_and_m(direction):
        harvest()
        plant(Entities.Bush)
        move(direction)
    while True:
        if num_items(Items.Wood) > wood_target:
            return True

        h_p_and_m(South)
        h_p_and_m(South)
        h_p_and_m(East)
        # End of first column, guaranteed to have grown bushes after first loop
        h_p_and_m(South)
        h_p_and_m(South)
        h_p_and_m(East)
        # End of second column, guaranteed to have grown bushes after first loop
        # Regular bush:
        h_p_and_m(South)
        # Get hay on the first run, possibly bushes have grown back if this
        # isn't the first pass of the farmland that we do. But we don't wait
        # for them if they didn't have enough time to grow. (Kinda greedy)
        harvest()
        move(South)
        # Get hay/bush, then backtrack:
        harvest()
        move(North)
        while not can_harvest(): # We wait for the hay to grow back
            pass
        h_p_and_m(South)
        h_p_and_m(East)

def carrot_three_by_three(carrot_target):
    CONST_WAIT_FOR_CARROTS = 3
    def h_p_and_m(direction, should_till=False):
        harvest()
        if should_till:
            till()
        plant(Entities.Carrots)
        move(direction)

    def hay_and_continue():
        for _ in range(CONST_WAIT_FOR_CARROTS):
            harvest()
            move(South)
            harvest()
            move(North)
        harvest()
        move(South)
        move(East)
    # initial setup:
    for _ in range(2):
        h_p_and_m(South, True)
        h_p_and_m(South, True)
        h_p_and_m(East, True)
    h_p_and_m(South, True)
    hay_and_continue()

    while True:
        if num_items(Items.Carrot) > carrot_target:
            return True
        elif num_items(Items.Carrot_Seed) < 7:
            quick_print("Seed issue @ carrot_three_by_three()")
            return False

        for _ in range(2):
            h_p_and_m(South)
            h_p_and_m(South)
            h_p_and_m(East)
        h_p_and_m(South)
        hay_and_continue()

def poly_farm(priority_as_item, target_amount, exclusive = True):
    # Initial setup:
    WORLD_TILE_COUNT = get_world_size()**2
    item_to_ent = {Items.Hay:Entities.Grass, Items.Carrot:Entities.Carrots,
                   Items.Wood:Entities.Tree} # Only these can be companions.
    priority_as_entity = item_to_ent[priority_as_item]
    companion_requests = {}
    for next_move in precalc:
        if get_ground_type() != Grounds.Soil:
            till()
        plant(priority_as_entity)
        move(next_move)

    while True: # Main loop
        acquire_seeds(Items.Carrot_Seed, WORLD_TILE_COUNT, False)

        for next_move in precalc: # Visit every tile once
            current_pos = (get_pos_x(),get_pos_y())
            if current_pos in companion_requests:
                harvest()
                plant(companion_requests.pop(current_pos))
            else:
                harvest()
                plant(priority_as_entity)

            if get_entity_type() != priority_as_entity and exclusive:
                move(next_move)
                continue
            new_comp = get_companion()
            companion_requests[(new_comp[1], new_comp[2])] = new_comp[0]
            move(next_move)

        if num_items(priority_as_item) > target_amount:
            return True

while True:
    print("° This file should be run from Method Tester.py")
