def grind_method(what, target_amount, ignore_power = False):
    quick_print("Now grinding: ", what, " required: ", target_amount)
    if what == Items.Power:
        get_power(target_amount)
    elif num_unlocked(Unlocks.Sunflowers) > 0 and num_items(Items.Power) < 50:
        if num_items(Items.Carrot) < get_world_size() **2:
            grind_method(Items.Carrot, get_world_size()**2)
        get_power(0) # There's a buffer of 50 implemented

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
                elif num_unlocked(Unlocks.Trees) > 0: # TODO: probably can make hay and trees instead of tree and bush
                    tree_and_bush(target_amount)
                else:
                    three_by_three_bush(target_amount)

            elif what == Items.Carrot: # TODO: add a better method for 3x3 stage
                # TODO: frontload seed acquistion here, as previously done with pumpkin seeds
                if num_unlocked(Unlocks.Trees) == 0:
                    carrots_ensure_seeds(target_amount)
                else:
                    if not carrots_trusting(target_amount): 
                        carrots_ensure_seeds(target_amount)
                        # TODO: Remove the check later if all tests are passed
        else:
            poly_farm(what, target_amount)
    
    elif what == Items.Pumpkin:
        cost_per_run = OPTIMAL_PUMPKIN_SEEDS[num_unlocked(Unlocks.Expand)]
        expected_yield_per_run = (get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins)
        needed_runs = (target_amount // expected_yield_per_run)
        acquire_seeds(Items.Pumpkin_Seed, needed_runs * cost_per_run)
        pumpkin_smart(target_amount)
    
    elif what == Items.Gold:
        do_simple_maze_run(target_amount)

    elif what == Items.Cactus:
        cactus_bubble(target_amount)

    elif what == Items.Bones:
        ultra_dumb_dyno(target_amount)


def get_me_unlock(what_unlock): 
    all_costs = get_cost(what_unlock)
    quick_print(what_unlock,"(", num_unlocked(what_unlock) + 1, ")", "requires:", all_costs)
    for resource in ORDER_OF_GRIND: # Grind in order of most expensive to cheapest
        if resource in all_costs:
            quick_print(all_costs[resource], "and we have:", num_items(resource))
            if num_items(resource) < all_costs[resource]:
                grind_method(resource, all_costs[resource])

    if not unlock(what_unlock): # Safety check
        print("We fucked up somewhere")
        get_me_unlock(what_unlock) # Recursion, spooky

while True:
    print("This file should never be run by itself")
