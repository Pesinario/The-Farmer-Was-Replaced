def wait_harv():
    while not can_harvest():
        if get_entity_type() == None:
            break
    harvest()

def smart_harv(debate=True):
    if can_harvest():
        harvest() 
    elif debate:
        debate_watering()

def till_this_many_tiles(how_many, debate=True): # TODO: this should be the LAST thing we swap to precalc
    for i in range(how_many):
        smart_harv(debate)
        if get_ground_type() != Grounds.Soil:
            till()
        walk_the_grid()

def acquire_seeds(type_of_seed, how_many):
    mustbuy = how_many - num_items(type_of_seed)
    if mustbuy < 0:
        return True

    if not trade(type_of_seed, mustbuy):
        # Farm the price of the seeds
        requirements = get_cost(type_of_seed)
        for seed_req in requirements:
            amount_required = requirements[seed_req]
            amount_required *= mustbuy
            if num_items(seed_req) < amount_required:
                grind_method(seed_req, amount_required)
        if not trade(type_of_seed, mustbuy):
            print("something went really wrong with seed acquisition")
            return False
    return True


def debate_watering(thresh=0.75):
    if get_water() <= thresh:
        if not use_item(Items.Water_Tank):
            can_buy = min(num_items(Items.Wood) // 5, 10)
            if not trade(Items.Empty_Tank, can_buy):
                print("Too broke to buy tanks")
            
def try_fert():
    if num_unlocked(Unlocks.Fertilizer) == 0:
        return False
    if not num_items(Items.Fertilizer) > 0:
        if not trade(Items.Fertilizer):
            pumpkin_smart(500)
    if use_item(Items.Fertilizer):
        return True
    else:
        return False
    
while True:
    print("This file should never be run by itself")
