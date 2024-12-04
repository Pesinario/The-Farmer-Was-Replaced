def reset_sunflowers():
    navigate_to(0,0)
    plant(Entities.Sunflower)
    harvest()

def old_method_sunflower(power_target):
    WORLD_TILE_COUNT = get_world_size()**2
    till_this_many_tiles(WORLD_TILE_COUNT)
    while True:
        biggest = 0
        acquire_seeds(Items.Sunflower_Seed, WORLD_TILE_COUNT)
        for i in range(WORLD_TILE_COUNT):
            plant(Entities.Sunflower)
            debate_watering(0.75)
            a = measure()
            if a == None:
                a = 0
            if a > biggest:
                biggest = a
            walk_the_grid()
        # print("biggest:", biggest)
        biggestThresh = biggest -3

        while biggest > biggestThresh: # harvest
            for i in range(WORLD_TILE_COUNT):
                if measure() == biggest:
                    smart_harv()
                walk_the_grid()
            biggest = biggest - 1
        reset_sunflowers()
        if num_items(Items.Power) > power_target:
            return True

def sunflower_no_replanting(should_setup):
    my_record = {}

    for next_move in precalc: # Initial setting up
        if should_setup:
            harvest()
            if get_ground_type() != Grounds.Soil:
                till()
        debate_watering(0.5)
        plant(Entities.Sunflower)
        petals = measure()
        if petals in my_record:
            petal_siblings = my_record.pop(petals)
            petal_siblings.append([get_pos_x(), get_pos_y()])
            my_record[petals] = petal_siblings
        elif petals == None:
            print("Some kind of error @ Sunflower Master")
        else:
            my_record[petals] = [[get_pos_x(), get_pos_y()]]
        move(next_move)

    for i in range(9): # harvest
        offset_petal = 15-i
        if offset_petal in my_record:
            siblings = my_record[offset_petal]
            for sunflower in siblings:
                navigate_smart(sunflower)
                wait_harv()
    
def get_power(power_target=0, initial=True):
    WORLD_TILE_COUNT = get_world_size()**2
    expected_yield = EXPECTED_POWER[num_unlocked(Unlocks.Expand)]
    runs_to_fulfil = ((power_target + 50) // expected_yield) + 1
    acquire_seeds(Items.Sunflower_Seed, (WORLD_TILE_COUNT) * runs_to_fulfil)
    for i in range(runs_to_fulfil):
        if initial:
            sunflower_no_replanting(True)
            initial = False
        else:
            sunflower_no_replanting(False)
        # reset_sunflowers()
        if num_items(Items.Sunflower_Seed) < WORLD_TILE_COUNT:
            print("Seed issue @ get_power")
    if num_items(Items.Power) < power_target + 50:
        print("We underfarmed sunflowers.")

while True:
    print("This file should be run from Method Tester.py")
