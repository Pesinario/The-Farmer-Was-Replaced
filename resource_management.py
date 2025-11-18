from utils import wait_harv, time_stamp
from farm_bones import snake_basic
from farm_cactus import cactus_shaker
from farm_gold import do_simple_maze_runs, maze_branch_based
from farm_power import get_power
from farm_pumpkins import pumpkin_smart, pumpkin_multi
from farm_trifecta import hay_vertical, hay_full_field
from farm_trifecta import tree_and_bush
from farm_trifecta import one_by_three_bush_hay_wait, three_by_three_with_hay
from farm_trifecta import carrots_trusting, carrot_three_by_three
from farm_trifecta import poly_farm

ORDER_OF_GRIND = [
    Items.Bone,
    Items.Cactus,
    Items.Gold,
    Items.Weird_Substance,
    Items.Pumpkin,
    Items.Power,
    Items.Carrot,
    Items.Wood,
    Items.Hay]

def grind_method(what, target_amount, boost=True, is_test=False):
    if num_items(what) > target_amount:
        return True

    random_id = random()
    if not is_test:
        quick_print("+ Now grinding:", what, "up to:", target_amount,
                    "boost active:", boost, "id:", random_id,
                    "timestamp:", time_stamp())

    if what != Items.Power:
        if num_unlocked(Unlocks.Sunflowers) > 0:
            if num_items(Items.Power) < 1:
                quick_print(
                    "° We're out of juice, that was an oopsie somewhere.")

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

    elif what == Items.Bone:
        report = grind_bones(target_amount)

    else:
        quick_print("° Gigantic blunder @ grind_method", what)

    if report and not is_test:  #pylint: disable=[E0606]
        quick_print("+ Finished grinding: ", what, "up to:", target_amount,
                    "boost active:", boost,
                    "id:", random_id,
                    "timestamp:", time_stamp())

    return report


def grind_trifecta(what, target_amount):
    # TODO: Be slightly smarter about how we farm the trifecta.

    if num_unlocked(Unlocks.Polyculture) != 0:
        poly_farm(what, target_amount)

    elif what == Items.Hay:
        if num_unlocked(Unlocks.Expand) < 1:
            for _ in range(target_amount):
                wait_harv()
        elif num_unlocked(Unlocks.Sunflowers) < 1:
            hay_vertical(target_amount)
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
        seeds = get_cost(Entities.Carrot) * runs_needed * WORLD_TILE_COUNT
        request_grind(seeds)

        if num_unlocked(Unlocks.Expand) < 3:
            carrot_three_by_three(target_amount)
        else:
            if not carrots_trusting(target_amount):
                while True:
                    quick_print("° Fix this correctly.")
        return num_items(what) > target_amount


def grind_pumpkins(target_amount):
    if max_drones() ==1:
        method = pumpkin_smart
    else:
        method = pumpkin_multi

    MAX_RUNS_ALLOWED = 9  # To prevent buying a huge amount of extra seeds.
    # We split our seed acquisition (and grind) to a maximum of 10.
    SEEDS_99_PERCENT = {2: 17, 3: 27, 4: 40,
                        5: 55, 6: 72, 7: 92, 8: 115, 9: 140}
    # This is the amount of seeds needed to get a 99% chance of harvesting a
    # full field of pumpkins without running out, according to Expand size.
    seeds_per_run = SEEDS_99_PERCENT[num_unlocked(Unlocks.Expand)]
    yield_per_run = ((get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins))
    needed_pumpkins = target_amount - num_items(Items.Pumpkin)
    needed_runs = needed_pumpkins // yield_per_run + 1  # Extra run for safety.
    pumpkin_run_tracker = 0
    while needed_runs > MAX_RUNS_ALLOWED:
        grind_method(Items.Carrot, MAX_RUNS_ALLOWED * seeds_per_run * get_cost(Entities.Pumpkin)[Items.Carrot])
        if not method(MAX_RUNS_ALLOWED, pumpkin_run_tracker):
            quick_print('° Error @grind_pumpkins during run splitting')
            return False
        needed_runs -= MAX_RUNS_ALLOWED
        pumpkin_run_tracker += MAX_RUNS_ALLOWED

    quick_print('$ About to try to get', needed_runs *
                seeds_per_run + seeds_per_run, 'Pumpkin seeds')
    grind_method(Items.Carrot, MAX_RUNS_ALLOWED * seeds_per_run * get_cost(Entities.Pumpkin)[Items.Carrot])
    quick_print('$ I have:', num_items(Items.Carrot), "For: ",
                needed_runs, "Runs at expand size",
                num_unlocked(Unlocks.Expand))
    if not method(needed_runs, pumpkin_run_tracker):
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

    gold_per_maze = num_unlocked(Unlocks.Mazes) * WORLD_TILE_COUNT
    remaining_gold_to_farm = target_amount - num_items(Items.Gold)
    mazes_for_goal = (remaining_gold_to_farm // gold_per_maze) + 1

    expected_weird_usage = mazes_for_goal * get_world_size() * (2 ** (num_unlocked(Unlocks.Mazes) - 1))
    if num_items(Items.Weird_Substance) < expected_weird_usage:
        quick_print(
            "+ About to grind",
            (expected_weird_usage - num_items(Items.Weird_Substance)),
            "Weird_Substance for fertilizer"
        )
        grind_method(Items.Weird_Substance, expected_weird_usage)
    else:
        quick_print("- Had enough Weird_Substance already")

    return do_simple_maze_runs(mazes_for_goal)
    # TODO: fix the smart mazes
    #if maze_branch_based(mazes_for_goal):
    #    quick_print("Fertilizer leftover:", num_items(Items.Fertilizer))
    #    return True
    #else:
    #    return False


def grind_cacti(target_amount):
    ensure_power()
    expected_yield = num_unlocked(Unlocks.Cactus) * get_world_size()**3
    runs_needed = target_amount // expected_yield
    if runs_needed == 0:
        runs_needed = 1
    cost = get_cost(Entities.Cactus)[Items.Pumpkin] * runs_needed * get_world_size() ** 2
    if cost > num_items(Items.Pumpkin):
        grind_method(Items.Pumpkin, cost)
    return cactus_shaker(target_amount)



def grind_bones(target_amount):  # TODO: check for cactus before starting
    ensure_power()
    return snake_basic(target_amount)

def ensure_power(how_much=None):
    # The logic here has room for improvement
    if how_much == None:
        expand = num_unlocked(Unlocks.Expand)
        if expand > 6: # Meaning we are at an 8x8 farm size
            how_much = 200
        elif expand == 3:
            how_much = 50
        else:
            how_much = 100

    if how_much > num_items(Items.Power):
        grind_method(Items.Power, how_much - num_items(Items.Power))


def request_grind(grind_what):
    for resource in ORDER_OF_GRIND:  # Grind in descending order of cost
        if resource in grind_what:
            if num_items(resource) < grind_what[resource]:
                quick_print("+ Sending grind order of",
                            resource, grind_what[resource])
                grind_method(resource, grind_what[resource])
            else:
                quick_print("- we're good on", resource)


if __name__ == "__main__":
    while True:
        print("° This file should be run from method_tester.py")
