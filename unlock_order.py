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

def new_route(): # TODO: WIP, should incorporate stockpiling of seeds BEFORE
    # upgrading carrots/pumpkins, since they'll be more expensive after.
    one_by_three   = [Unlocks.Speed, Unlocks.Expand , Unlocks.Plant,
                      Unlocks.Expand, Unlocks.Grass]
    three_by_three = [Unlocks.Speed, Unlocks.Carrots, Unlocks.Trees,
                      Unlocks.Speed, Unlocks.Speed, Unlocks.Expand]
    four_by_four   = [Unlocks.Sunflowers, Unlocks.Speed, Unlocks.Grass,
                    Unlocks.Carrots, Unlocks.Trees, Unlocks.Pumpkins,
                    Unlocks.Fertilizer, Unlocks.Expand]
    five_by_five   = [Unlocks.Polyculture, Unlocks.Expand]

    my_route = one_by_three + three_by_three + four_by_four + five_by_five
    return my_route

def route_stolen_from_josh_from_the_discord():
    # this order of unlocks was taken from legoman12343, as posted in the
    # official "The Farmer Was Replaced" discord, it will not be the final
    # route but it is definitely better than the old one
    stolen=[]
    stolen.append(Unlocks.Grass)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Expand)
    stolen.append(Unlocks.Plant)
    stolen.append(Unlocks.Expand)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Grass)
    stolen.append(Unlocks.Carrots)
    stolen.append(Unlocks.Trees)
    stolen.append(Unlocks.Trees)
    stolen.append(Unlocks.Expand)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Carrots)
    stolen.append(Unlocks.Sunflowers)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Grass)
    stolen.append(Unlocks.Grass)
    stolen.append(Unlocks.Trees)
    stolen.append(Unlocks.Trees)
    stolen.append(Unlocks.Carrots)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Carrots)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Pumpkins)
    stolen.append(Unlocks.Polyculture)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Carrots)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Pumpkins)
    stolen.append(Unlocks.Pumpkins)
    stolen.append(Unlocks.Pumpkins)
    stolen.append(Unlocks.Expand)
    stolen.append(Unlocks.Expand)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Carrots)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Speed)
    stolen.append(Unlocks.Trees)
    stolen.append(Unlocks.Pumpkins)
    stolen.append(Unlocks.Pumpkins)
    stolen.append(Unlocks.Expand)
    stolen.append(Unlocks.Fertilizer)
    stolen.append(Unlocks.Expand)
    stolen.append(Unlocks.Mazes)
    stolen.append(Unlocks.Mazes)
    stolen.append(Unlocks.Mazes)
    stolen.append(Unlocks.Cactus)
    stolen.append(Unlocks.Cactus)
    stolen.append(Unlocks.Dinosaurs)
    stolen.append(Unlocks.Dinosaurs)
    stolen.append(Unlocks.Leaderboard)
    return stolen


def get_me_best_route():
    return route_stolen_from_josh_from_the_discord()
