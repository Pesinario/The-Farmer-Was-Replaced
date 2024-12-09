def grind_method(what, target_amount, boost = True, is_test = False):
    random_id = random()
    if not is_test:
        quick_print("+ Now grinding: ", what, "up to:", target_amount,
                    "boost active:", boost, "id:", random_id,
                    "timestamp:", time_stamp())

    if what != Items.Power:
        if num_unlocked(Unlocks.Sunflowers) > 0:
            if num_items(Items.Power) < 1:
                quick_print("° We're out of juice, that was an oopsie somewhere.")

            if num_items(Items.Power) < 50 and boost:
                quick_print("+ Getting power before getting", what)
                ensure_power()

    if what == Items.Power:
        report = get_power(target_amount)

    elif what in [Items.Hay, Items.Wood, Items.Carrot]:
        report = grind_trifecta(what, target_amount)

    elif what == Items.Pumpkin:
        report = grind_pumpkins(target_amount)

    elif what == Items.Gold:
        report = grind_gold(target_amount)

    elif what == Items.Cactus:
        report = grind_cacti(target_amount)

    elif what == Items.Bones:
        report = grind_bones(target_amount)

    else:
        quick_print("° Gigantic blunder @ grind_method", what)

    if report and not is_test: # pylint: disable=[E0606]
        quick_print("+ Finished grinding: ", what, "up to:", target_amount,
                    "boost active:", boost, "id:", random_id, "timestamp:", time_stamp())

    return report

def grind_trifecta(what, target_amount): # TODO: Be slightly smarter about how
    # we farm the trifecta.
    if num_unlocked(Unlocks.Polyculture) != 0:
        poly_farm(what, target_amount)

    elif what == Items.Hay:
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
            three_by_three_with_hay(target_amount)

    elif what == Items.Carrot:
        WORLD_TILE_COUNT = get_world_size()**2
        carrots_required = target_amount - num_items(what)
        yield_per_run = num_unlocked(Unlocks.Carrots) * WORLD_TILE_COUNT
        runs_needed = carrots_required // yield_per_run
        acquire_seeds(Items.Carrot_Seed, (runs_needed * WORLD_TILE_COUNT) + 1)
        if num_unlocked(Unlocks.Expand) < 3:
            carrot_three_by_three(target_amount)
        else:
            if not carrots_trusting(target_amount):
                while True:
                    print("° Fix this correctly.")
        return num_items(what) > target_amount

def grind_pumpkins(target_amount):
    MAX_RUNS_ALLOWED = 9 # To prevent buying a huge amount of extra seeds.
    # We split our seed acquisition (and grind) to a maximum of 10.
    SEEDS_99_PERCENT = {2:17, 3:27, 4:40, 5:55, 6:72, 7:92, 8:115, 9:140}
    # This is the amount of seeds needed to get a 99% chance of harvesting a
    # full field of pumpkins without running out, according to Expand size.
    cost_per_run = SEEDS_99_PERCENT[num_unlocked(Unlocks.Expand)]
    yield_per_run = ((get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins))
    needed_pumpkins = target_amount - num_items(Items.Pumpkin)
    needed_runs = needed_pumpkins // yield_per_run + 1 # Extra run for safety.

    while needed_runs > MAX_RUNS_ALLOWED:
        acquire_seeds(Items.Pumpkin_Seed,
                      MAX_RUNS_ALLOWED * cost_per_run + cost_per_run)
        if not pumpkin_smart(MAX_RUNS_ALLOWED):
            quick_print('° Error @grind_pumpkins during run splitting')
            return False
        needed_runs -= MAX_RUNS_ALLOWED

    acquire_seeds(Items.Pumpkin_Seed,
                  needed_runs * cost_per_run + cost_per_run)
    if not pumpkin_smart(needed_runs):
        quick_print('° Error @grind_pumpkins near the end')
        return False

    if num_items(Items.Pumpkin) > target_amount:
        return True
    else:
        quick_print("° Error @grind_pumpkins, ",
                    "Somehow we didn't farm enough pumpkins.")
        return False

def grind_gold(target_amount):
    ensure_power()
    WORLD_TILE_COUNT = get_world_size()**2
    MAX_MAZES_ALLOWED = 20
    FERT_PER_MAZE = 25 # An estimation of how much fertilizer we'll need.
    MAX_FERT_PER_BATCH = FERT_PER_MAZE * MAX_MAZES_ALLOWED
    # TODO: Simulate this also.
    gold_per_maze = num_unlocked(Unlocks.Mazes) * WORLD_TILE_COUNT
    remaining_gold_to_farm = target_amount - num_items(Items.Gold)
    mazes_for_goal = (remaining_gold_to_farm // gold_per_maze) + 1
    expected_fert_usage = mazes_for_goal * FERT_PER_MAZE
    trade(Items.Fertilizer, num_items(Items.Pumpkin) // 10) # At this point,
    # we only need the pumpkins for fertilizer, so we can spend them all.
    if mazes_for_goal * expected_fert_usage < num_items(Items.Fertilizer):
        if not do_simple_maze_run(target_amount):
            quick_print("° ERROR while farming gold")
            return False
        else:
            quick_print("$ We finished grinding gold, we have",
                        num_items(Items.Fertilizer), "Fertilizer leftover.")
            return True

    else:
        quick_print("- We are about to attempt to grind and buy",
                    MAX_FERT_PER_BATCH - num_items(Items.Fertilizer),
                    "Fertilizer for farming gold")
        while mazes_for_goal > MAX_MAZES_ALLOWED:
            acquire_seeds(Items.Fertilizer, FERT_PER_MAZE, MAX_MAZES_ALLOWED)
            if not do_simple_maze_run(
                num_items(Items.Gold) +
                gold_per_maze * MAX_MAZES_ALLOWED
                ):
                quick_print("° ERROR while farming gold")
                return False
            mazes_for_goal -= MAX_MAZES_ALLOWED
        acquire_seeds(Items.Fertilizer, mazes_for_goal * FERT_PER_MAZE)
        if not do_simple_maze_run(target_amount):
            quick_print("° ERROR while farming gold")
            return False
        else:
            return True

def grind_cacti(target_amount):
    ensure_power()
    expected_yield = num_unlocked(Unlocks.Cactus) * get_world_size()**3
    runs_needed = target_amount // expected_yield
    if acquire_seeds(Items.Cactus_Seed, runs_needed * get_world_size()**2):
        return cactus_shaker(target_amount)
    else:
        quick_print("° Cactus seed acquisition Issue")
        return False

def grind_bones(target_amount):
    ensure_power()
    bones_per_dino = 4 * num_unlocked(Unlocks.Dinosaurs)
    needed_eggs_safe = ((target_amount - num_items(Items.Egg))
                        // bones_per_dino
                        + get_world_size()**2)
    if acquire_seeds(Items.Egg, needed_eggs_safe):
        ensure_power()
        return dyno_slightly_smarter(target_amount)
    else:
        return False


def ensure_power(how_much = None):
    # TODO: make some clever logic here
    if how_much == None:
        how_much = 200

    if how_much > num_items(Items.Power):
        grind_method(Items.Power, how_much - num_items(Items.Power))

def acquire_seeds(type_of_seed, how_many, grind = True):
    quick_print("- acquire_seeds got a request of", how_many, type_of_seed)
    seed_diff = how_many - num_items(type_of_seed)
    if seed_diff < 0:
        quick_print("- we had more than", how_many, type_of_seed, "already.")
        return True

    if not trade(type_of_seed, seed_diff):
        if not grind:
            quick_print("- was not able to buy the seeds and will not grind.")
            return False
        # Farm the price of the seeds
        requirements = get_cost(type_of_seed)
        for material in requirements:
            requirements[material] = requirements[material] * seed_diff
        quick_print("- Couldn't afford", seed_diff, type_of_seed,
                    "Starting to grind up to", requirements, "@ acquire_seeds()")
        if type_of_seed == Items.Sunflower_Seed:
            quick_print(
                "° Not enough carrots to farm power even once.",
                "Attempting to grind carrots for sunflower seeds without boost"
                )
            grind_method(Items.Carrot, seed_diff, False)
        else:
            grind_by_order(requirements)
        if not trade(type_of_seed, seed_diff):
            print("° Something went really wrong with seed acquisition, ",
                  "even after trying to grind them.")
            return False
    else:
        quick_print("- was able to buy", how_many, type_of_seed, "without grinding")
        return True

def grind_by_order(grind_what):
    for resource in ORDER_OF_GRIND: # Grind in descending order of cost
        if resource in grind_what:
            if num_items(resource) < grind_what[resource]:
                quick_print("+ Sending grind order of",
                            resource, grind_what[resource])
                grind_method(resource, grind_what[resource])
            else:
                quick_print("- we're good on", resource)

while True:
    print("° This file should never be run by itself")
