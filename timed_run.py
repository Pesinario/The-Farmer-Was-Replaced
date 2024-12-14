from resource_management import grind_by_order
from navigation import precalc_world
from unlock_order import get_me_best_route


timed_reset()
START_TIME = get_time()
quick_print("~", "Start time is", START_TIME)

# Output keys:
# ° means error
# $ means it could be possible to cut corners here
# ~ means milestone
# + means grinding Something
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
            print("° We fucked up somewhere")


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
            print("°", current_milestone_chased)
    if current_milestone_chased == Unlocks.Expand:
        precalc = precalc_world()  # I don't think we should need this before
        # we get to at least 3x3 farm size.

quick_print("~", "End time is", time_stamp())
report_extra_resources()
quick_print("~ End of Log")
timed_reset()
