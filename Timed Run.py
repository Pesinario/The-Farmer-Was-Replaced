timed_reset()
START_TIME = get_time()

KINDS_OF_UNLOCKS = [Unlocks.Speed, Unlocks.Expand, Unlocks.Plant, Unlocks.Grass, 
                     Unlocks.Trees, Unlocks.Carrots, Unlocks.Sunflowers, 
                     Unlocks.Pumpkins, Unlocks.Polyculture, Unlocks.Fertilizer, 
                     Unlocks.Mazes, Unlocks.Cactus, Unlocks.Dinosaurs, 
                     Unlocks.Leaderboard]

BEFORE_CARROTS = [Unlocks.Speed, Unlocks.Expand, Unlocks.Plant, Unlocks.Expand, Unlocks.Speed, Unlocks.Grass, Unlocks.Carrots]
BEFORE_TREES = [Unlocks.Expand, Unlocks.Speed, Unlocks.Trees]
BEFORE_SUNFLOWERS = [Unlocks.Speed, Unlocks.Grass, Unlocks.Trees, Unlocks.Carrots, Unlocks.Speed, Unlocks.Sunflowers]
PUMPKIN_RELATED = [Unlocks.Pumpkins, Unlocks.Fertilizer, Unlocks.Expand, Unlocks.Expand]
POLY_TIME = [Unlocks.Speed, Unlocks.Polyculture, Unlocks.Grass, Unlocks.Trees, Unlocks.Carrots, Unlocks.Pumpkins, Unlocks.Expand, Unlocks.Expand, Unlocks.Mazes]
STORY_END = [Unlocks.Mazes, Unlocks.Cactus, Unlocks.Dinosaurs, Unlocks.Leaderboard]


GAME_PLAN = BEFORE_CARROTS + BEFORE_TREES + BEFORE_SUNFLOWERS + PUMPKIN_RELATED + POLY_TIME + STORY_END
# Since this is now public: please read: the route is TERRIBLE! it looks like that for ease of tweaking

log_of_milestones = {"start":0} # TODO: this should be overhauled
milestone_counter = 0

def hard_coded_milestone(milestone_name, started_at_time):
    took_this_long = get_time() - started_at_time
    log_of_milestones[milestone_name] = took_this_long

def log_this_unlock(unlock): # adds to the dictionary the unlock and how long it took
    started_unlocking = get_time()
    get_me_unlock(unlock)
    took_this_long = (unlock,get_time() - started_unlocking)
    log_of_milestones[milestone_counter] = took_this_long
    quick_print(current_milestone_chased, "started @", started_unlocking-START_TIME, "ended @", get_time()-START_TIME, "and took", took_this_long)
    return milestone_counter + 1

precalc = [] # This is global!

for current_milestone_chased in GAME_PLAN:
    if current_milestone_chased in KINDS_OF_UNLOCKS:
        milestone_counter = log_this_unlock(current_milestone_chased)
    else:
        while True:
            print(current_milestone_chased)
    if current_milestone_chased == Unlocks.Expand:
        precalc = precalc_world() # I don't think we should need this before we get to at least 4x4 farm size, but we define it as soon as we get 1x3


quick_print(log_of_milestones)
timed_reset()