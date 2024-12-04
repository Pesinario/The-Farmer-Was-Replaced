def grind_method(what, target_amount, boost = True):
    quick_print("+ Now grinding: ", what, " required: ", target_amount, "boost active:", boost)
    WORLD_TILE_COUNT = get_world_size()**2
    if what == Items.Power:
        get_power(target_amount)
    elif num_unlocked(Unlocks.Sunflowers) > 0 and num_items(Items.Power) < 50 and boost:
        quick_print("+ Getting power before getting", what)
        if num_items(Items.Carrot) < WORLD_TILE_COUNT: # sunflower seeds cost 1 carrot each
            quick_print(
                "+-° Not enough carrots to farm power even once.",
                "Attempting to grind carrots for sunflower seeds without boost"
                )
            grind_method(Items.Carrot, WORLD_TILE_COUNT, False)
        get_power(0) # There's a buffer of 50 implemented

    if what in [Items.Hay, Items.Wood, Items.Carrot]:
        if num_unlocked(Unlocks.Polyculture) == 0:
            if what == Items.Hay:
                if num_unlocked(Unlocks.Expand) < 1:
                    for _ in range(target_amount):
                        wait_harv()
                elif num_unlocked(Unlocks.Sunflowers) < 1:
                    harv_hay_dumb(target_amount)
                else:
                    hay_full_field(target_amount)

            elif what == Items.Wood:
                if num_unlocked(Unlocks.Expand) == 1:
                    one_by_three_bush_hay_wait(target_amount)
                elif num_unlocked(Unlocks.Trees) > 0:
                    tree_and_bush(target_amount)
                else:
                    three_by_three_bush(target_amount)

            elif what == Items.Carrot: # TODO: add a better method for 3x3 stage
                if num_unlocked(Unlocks.Trees) > 0:
                    carrots_required = target_amount - num_items(what)
                    runs_needed = carrots_required // (num_unlocked(Unlocks.Carrots) * WORLD_TILE_COUNT)
                    acquire_seeds(Items.Carrot_Seed, (runs_needed * WORLD_TILE_COUNT) + WORLD_TILE_COUNT)
                    if not carrots_trusting(target_amount):
                        while True:
                            print("° Fix this correctly.")
                else:
                    carrots_ensure_seeds(target_amount)
        else:
            poly_farm(what, target_amount)

    elif what == Items.Pumpkin:
        cost_per_run = OPTIMAL_PUMPKIN_SEEDS[num_unlocked(Unlocks.Expand)]
        expected_yield_per_run = (get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins)
        needed_runs = target_amount // expected_yield_per_run
        acquire_seeds(Items.Pumpkin_Seed, needed_runs * cost_per_run)
        pumpkin_smart(target_amount)

    elif what == Items.Gold:
        FERT_PER_MAZE = 25 # This value is just a guess
        gold_per_maze = num_unlocked(Unlocks.Mazes) * WORLD_TILE_COUNT
        remaining_gold_to_farm = target_amount - num_items(Items.Gold)
        mazes_for_goal = (remaining_gold_to_farm // gold_per_maze) + 1
        expected_fert_usage = mazes_for_goal * FERT_PER_MAZE
        must_get_fert = expected_fert_usage - num_items(Items.Fertilizer)
        quick_print("$ We are about to buy", expected_fert_usage, "Fertilizer for farming gold")
        if num_items(Items.Fertilizer) < expected_fert_usage:
            if not trade(Items.Fertilizer, must_get_fert):
                grind_method(Items.Pumpkin, must_get_fert * 10)
            if not trade(Items.Fertilizer, must_get_fert):
                print("° FAILED TWICE TO BUY FERTILIZER.")
        do_simple_maze_run(target_amount)
        quick_print("$ We finished grinding gold, we have", num_items(Items.Fertilizer), "Fertilizer leftover.")

    elif what == Items.Cactus:
        cactus_bubble(target_amount)

    elif what == Items.Bones:
        expected_bones_per_chicken = 4 * num_unlocked(Unlocks.Dinosaurs)
        needed_eggs_safe = ((2000 - num_items(Items.Egg)) // expected_bones_per_chicken ) + WORLD_TILE_COUNT
        acquire_seeds(Items.Egg, needed_eggs_safe)
        dyno_slightly_smarter(target_amount)


def get_me_unlock(what_unlock):
    all_costs = get_cost(what_unlock)
    quick_print("+", what_unlock, num_unlocked(what_unlock) + 1, "requires:", all_costs)
    for resource in ORDER_OF_GRIND: # Grind in order of most expensive to cheapest
        if resource in all_costs:
            quick_print("+", all_costs[resource], "and we have:", num_items(resource))
            if num_items(resource) < all_costs[resource]:
                grind_method(resource, all_costs[resource])

    if not unlock(what_unlock): # Safety check
        print("° We fucked up somewhere")
        get_me_unlock(what_unlock) # Recursion, spooky

while True:
    print("° This file should never be run by itself")
