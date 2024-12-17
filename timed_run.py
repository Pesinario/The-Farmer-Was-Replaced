from resource_management import grind_by_order, grind_method, ensure_power
from navigation import precalc_world
from unlock_order import get_me_best_route


timed_reset()
START_TIME = get_time()
quick_print("~", "Start time is", START_TIME)

# Output keys:
# ° means error
# $ means possible to cut corners, maybe
# ~ means milestone
# + means grinding something
# - means info


def time_stamp():
    return get_time() - START_TIME


def report_extra_resources():
    my_extras = {}
    for extra in ORDER_OF_GRIND:
        if num_items(extra) > 0:
            my_extras[extra] = num_items(extra)
    quick_print("$ Extra resources:", my_extras)


def get_me_unlock(what_unlock):
    all_costs = get_cost(what_unlock)
    quick_print("+", what_unlock, num_unlocked(what_unlock) +
                1, "requires:", all_costs)
    grind_by_order(all_costs)

    return unlock(what_unlock)


def do_final():
    # This is some hardcoded stuff that we call after unlocking mazes.
    # It has room for improvement.
    ensure_power(1500)
    quick_print("~ Started mazes at:", time_stamp())
    while num_items(Items.Gold)< 50000:
        grind_method(Items.Gold, 50000)
    quick_print("~ Finished mazes stage at:", time_stamp())

    # ensure_power(1000)
    unlock(Unlocks.Cactus)
    if not trade(Items.Cactus_Seed, 3050):
        quick_print("° Couldn't pre-buy cactus seeds")
    unlock(Unlocks.Cactus)
    quick_print("~ Started grinding cacti at:", time_stamp())
    grind_method(Items.Cactus, 12280)
    quick_print("~ Finished grinding cacti at:", time_stamp())
    # ensure_power(500)
    unlock(Unlocks.Dinosaurs)
    if not trade(Items.Egg, 314):
        quick_print("° Couldn't pre-buy eggs")
    unlock(Unlocks.Dinosaurs)
    # unlock(Unlocks.Dinosaurs)
    grind_method(Items.Bones, 2000)

    unlock(Unlocks.Leaderboard)

# adds to the dictionary the unlock and how long it took
def log_this_unlock(current_unlock):
    successfully_unlocked = False
    attempts = 0
    started_unlocking = get_time()
    quick_print("~", current_milestone_chased, "started @",
                started_unlocking - START_TIME)
    while not successfully_unlocked:
        attempts += 1
        if get_me_unlock(current_unlock):
            took_this_long = get_time() - started_unlocking
            quick_print(
                "~", current_milestone_chased, num_unlocked(current_unlock),
                "ended @", get_time() - START_TIME,
                "and took", took_this_long,
                "attempts:", attempts
            )
            report_extra_resources()
            return True
        else:
            quick_print("° Somewhere along the way, we made a critical mistake",
                  "and cannot afford the upgrade.")


KINDS_OF_UNLOCKS = [Unlocks.Speed, Unlocks.Expand, Unlocks.Plant,
                    Unlocks.Grass, Unlocks.Trees, Unlocks.Carrots,
                    Unlocks.Sunflowers, Unlocks.Pumpkins, Unlocks.Polyculture,
                    Unlocks.Fertilizer, Unlocks.Mazes, Unlocks.Cactus,
                    Unlocks.Dinosaurs, Unlocks.Leaderboard]

GAME_PLAN = get_me_best_route()  # This is the route we will attempt
precalc = []
# This is ordered from most expensive to least expensive.
# this way, we minimize "backtracking" while grinding resources.
ORDER_OF_GRIND = [Items.Bones, Items.Cactus, Items.Gold,
                  Items.Pumpkin, Items.Power,
                  Items.Carrot, Items.Wood, Items.Hay]

for current_milestone_chased in GAME_PLAN:
    if current_milestone_chased in KINDS_OF_UNLOCKS:
        log_this_unlock(current_milestone_chased)
    else:
        while True:
            quick_print("°", current_milestone_chased)
    if current_milestone_chased == Unlocks.Expand:
        precalc = precalc_world()  # I don't think we should need this before
        # we get to at least 3x3 farm size.
do_final()
quick_print("~", "End time is", time_stamp())
report_extra_resources()
quick_print("~ End of Log")
timed_reset()
