def grind_method(what, target_amount, precalc):
    if what == Items.Power:
        while num_items(Items.Power) < target_amount:
            do_power_run(target_amount, precalc)
    elif num_unlocked(Unlocks.Sunflowers) > 0 and num_items(Items.Power) < 50:
        do_power_run(0 , precalc)

    if what in [Items.Hay, Items.Wood, Items.Carrot]:
        if num_unlocked(Unlocks.Polyculture) == 0:
            if what == Items.Hay:
                if num_unlocked(Unlocks.Expand) < 1:
                    for i in range(target_amount):
                        wait_harv()
                else:
                    harv_hay_dumb(target_amount)

            elif what == Items.Wood:
                if num_unlocked(Unlocks.Expand) == 1:
                    one_by_three_bush(target_amount)
                elif num_unlocked(Unlocks.Trees) > 0:
                    tree_and_bush(target_amount)
                else:
                    three_by_three_bush(target_amount, precalc)

            elif what == Items.Carrot: # TODO: add a better method for 3x3 stage
                if num_unlocked(Unlocks.Trees) == 0:
                    carrots_ensure_seeds(target_amount, precalc)
                else:
                    if not carrots_trusting(target_amount, precalc): 
                        carrots_ensure_seeds(target_amount, precalc)
                        # TODO: Remove the check later if all tests are passed
        else:
            poly_farm(what, target_amount, precalc)
    
    elif what == Items.Pumpkin:
        pumpkin_smart(target_amount)
    
    elif what == Items.Gold:
        do_simple_maze_run(target_amount)

    elif what == Items.Cactus:
        cactus_bubble(target_amount)

    elif what == Items.Bones:
        ultra_dumb_dyno(target_amount, precalc)


def get_me_unlock(what_unlock, precalc): # TODO: time each of the farming steps maybe?
    all_costs = get_cost(what_unlock)
    quick_print(what_unlock,"(", num_unlocked(what_unlock) + 1, ")", "requires:", all_costs)
    for resource in all_costs: # i cant use reversed() :'(
        if num_items(resource) < all_costs[resource]:
            grind_method(resource, all_costs[resource], precalc)

    if not unlock(what_unlock): # Safety check
        print("We fucked up somewhere")
        get_me_unlock(what_unlock, precalc) # Recursion, spooky

while True:
    print("This file should never be run by itself")
