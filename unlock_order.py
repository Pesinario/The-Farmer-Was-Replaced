def old_route():
    before_carrots = [Unlocks.Speed, Unlocks.Expand, Unlocks.Plant,
                      Unlocks.Expand, Unlocks.Speed, Unlocks.Grass, Unlocks.Carrots]
    before_trees = [Unlocks.Trees, Unlocks.Expand, Unlocks.Speed]
    before_sunflowers = [Unlocks.Speed, Unlocks.Grass, Unlocks.Trees,
                         Unlocks.Carrots, Unlocks.Speed, Unlocks.Sunflowers]
    pumpkin_related = [Unlocks.Pumpkins, Unlocks.Fertilizer, Unlocks.Expand, Unlocks.Expand]
    poly_time = [Unlocks.Speed, Unlocks.Polyculture, Unlocks.Grass, Unlocks.Trees,
                 Unlocks.Carrots, Unlocks.Pumpkins, Unlocks.Expand, Unlocks.Expand, Unlocks.Mazes]
    story_end = [Unlocks.Mazes, Unlocks.Cactus, Unlocks.Dinosaurs, Unlocks.Leaderboard]
    my_route = (
        before_carrots + before_trees + before_sunflowers +
        pumpkin_related + poly_time + story_end
        )
    return my_route

def new_route():
    one_by_three   = [Unlocks.Speed, Unlocks.Expand , Unlocks.Plant,
                      Unlocks.Expand, Unlocks.Grass]
    three_by_three = [Unlocks.Speed, Unlocks.Carrots, Unlocks.Trees,
                      Unlocks.Speed, Unlocks.Speed, Unlocks.Expand]
    four_by_four   = [Unlocks.Sunflowers, Unlocks.Speed, Unlocks.Grass, Unlocks.Carrots, Unlocks.Trees, Unlocks.Pumpkins, Unlocks.Fertilizer, Unlocks.Expand]
    five_by_five   = [Unlocks.Polyculture, Unlocks.Expand]

    my_route = one_by_three + three_by_three + four_by_four + five_by_five
    return my_route


def get_me_best_route():
    return old_route()
