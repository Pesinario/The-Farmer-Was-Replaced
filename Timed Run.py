timed_reset()
START_TIME = get_time()
quick_print("$", "Start time is", START_TIME)

# Output keys:
# ° means error
# $ means it could be possible to cut corners here
# ~ means milestone
# + means grinding Something
# - means info

KINDS_OF_UNLOCKS = [Unlocks.Speed, Unlocks.Expand, Unlocks.Plant, Unlocks.Grass,
                     Unlocks.Trees, Unlocks.Carrots, Unlocks.Sunflowers,
                     Unlocks.Pumpkins, Unlocks.Polyculture, Unlocks.Fertilizer,
                     Unlocks.Mazes, Unlocks.Cactus, Unlocks.Dinosaurs,
                     Unlocks.Leaderboard]

BEFORE_CARROTS = [Unlocks.Speed, Unlocks.Expand, Unlocks.Plant, Unlocks.Expand,
                   Unlocks.Speed, Unlocks.Grass, Unlocks.Carrots]
BEFORE_TREES = [Unlocks.Expand, Unlocks.Speed, Unlocks.Trees]
BEFORE_SUNFLOWERS = [Unlocks.Speed, Unlocks.Grass, Unlocks.Trees,
                      Unlocks.Carrots, Unlocks.Speed, Unlocks.Sunflowers]
PUMPKIN_RELATED = [Unlocks.Pumpkins, Unlocks.Fertilizer, Unlocks.Expand, Unlocks.Expand]
POLY_TIME = [Unlocks.Speed, Unlocks.Polyculture, Unlocks.Grass, Unlocks.Trees,
              Unlocks.Carrots, Unlocks.Pumpkins, Unlocks.Expand, Unlocks.Expand, Unlocks.Mazes]
STORY_END = [Unlocks.Mazes, Unlocks.Cactus, Unlocks.Dinosaurs, Unlocks.Leaderboard]

GAME_PLAN = BEFORE_CARROTS + BEFORE_TREES + BEFORE_SUNFLOWERS + (
    PUMPKIN_RELATED + POLY_TIME + STORY_END)
# TODO: This route is awful.

def log_this_unlock(unlock): # adds to the dictionary the unlock and how long it took
    started_unlocking = get_time()
    quick_print("~", current_milestone_chased, "started @", started_unlocking - START_TIME)
    get_me_unlock(unlock)
    took_this_long = get_time() - started_unlocking
    quick_print("~", current_milestone_chased, "ended @", get_time() - START_TIME,
                 "and took", took_this_long)
    return True

# Some useful globals:
precalc = []
# These numbers came from simulations i ran:
OPTIMAL_PUMPKIN_SEEDS = {2:17, 3:27, 4:40, 5:55, 6:72, 7:92, 8:115, 9:140}
EXPECTED_POWER = {2:18.31, 3:46.97, 4:73.63, 5:126.14, 6:191.86, 7:281.47, 8:397.77, 9:544.71}
# This is ordered from most expensive to least expensive, to minimize recursion.
ORDER_OF_GRIND = [Items.Bones, Items.Cactus, Items.Gold, Items.Pumpkin,
                  Items.Pumpkin, Items.Power, Items.Carrot, Items.Wood, Items.Hay]

for current_milestone_chased in GAME_PLAN:
    if current_milestone_chased in KINDS_OF_UNLOCKS:
        log_this_unlock(current_milestone_chased)
    else:
        while True:
            print("°", current_milestone_chased)
    if current_milestone_chased == Unlocks.Expand:
        precalc = precalc_world() # I don't think we should need this before
        # we get to at least 4x4 farm size, but we define it as soon as we get 1x3

quick_print("$", "End time is", get_time())
timed_reset()
