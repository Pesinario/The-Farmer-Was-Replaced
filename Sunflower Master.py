def reset_sunflowers():
    navigate_to(0,0)
    trade(Items.Sunflower_Seed)
    plant(Entities.Sunflower)
    harvest()

def old_method_sunflower():
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


def new_method_sunflower():
    WORLD_TILE_COUNT = get_world_size()**2
    my_record = {}
    acquire_seeds(Items.Sunflower_Seed, WORLD_TILE_COUNT*1.5)
    for i in range(WORLD_TILE_COUNT): # Initial setting up
        harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Sunflower)
        petals = measure()
        if petals in my_record:
            petal_siblings = my_record.pop(petals)
            petal_siblings.append([get_pos_x(), get_pos_y()])
            my_record[petals] = petal_siblings
        else:
            my_record[petals] = [[get_pos_x(), get_pos_y()]]
        walk_the_grid()

    for i in range(5):
        offset_petal = 15-i
        if offset_petal in my_record:
            siblings = my_record[offset_petal]
            for sunflower in siblings:
                navigate_smart(sunflower)
                wait_harv()
    reset_sunflowers()
    
def do_power_run(power_target=0):
    MINIMUM_POWER = 50
    while power_target + MINIMUM_POWER > num_items(Items.Power):
        new_method_sunflower()

do_power_run(num_items(Items.Power) + 10000)