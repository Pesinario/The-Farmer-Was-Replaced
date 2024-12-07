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

def till_this_many_tiles(how_many, debate=True): # This is deprecated,
    # but is still used by some also deprected farming methods.
    for _ in range(how_many):
        smart_harv(debate)
        if get_ground_type() != Grounds.Soil:
            till()
        walk_the_grid()

def debate_watering(thresh=0.75):
    if get_water() <= thresh:
        if not use_item(Items.Water_Tank):
            can_buy = min(num_items(Items.Wood) // 5, 10)
            if not trade(Items.Empty_Tank, can_buy):
                print("- Too broke to buy tanks")

def try_fert():
    if num_items(Items.Fertilizer) < 1:
        if num_unlocked(Unlocks.Fertilizer) == 0:
            return False
        if num_items(Items.Pumpkin) < 10:
            return False
        if not trade(Items.Fertilizer, min((num_items(Items.Pumpkin) // 10), 100)):
            return False

    return use_item(Items.Fertilizer)

while True:
    print("° This file should never be run by itself")
