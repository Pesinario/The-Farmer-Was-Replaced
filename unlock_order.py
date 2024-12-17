def old_route():
    before_carrots = [Unlocks.Speed, Unlocks.Expand, Unlocks.Plant,Unlocks.Expand, Unlocks.Speed, Unlocks.Grass, Unlocks.Carrots]
    before_trees = [Unlocks.Trees, Unlocks.Expand, Unlocks.Speed]
    before_sunflowers = [Unlocks.Speed, Unlocks.Grass, Unlocks.Trees,Unlocks.Carrots, Unlocks.Speed, Unlocks.Sunflowers]
    pumpkin_related = [Unlocks.Pumpkins, Unlocks.Fertilizer, Unlocks.Expand, Unlocks.Expand]
    poly_time = [Unlocks.Speed, Unlocks.Polyculture, Unlocks.Grass, Unlocks.Trees,Unlocks.Carrots, Unlocks.Pumpkins, Unlocks.Expand, Unlocks.Expand, Unlocks.Mazes]
    story_end = [Unlocks.Mazes, Unlocks.Cactus, Unlocks.Dinosaurs, Unlocks.Leaderboard]
    my_route = (before_carrots + before_trees + before_sunflowers +pumpkin_related + poly_time + story_end)
    return my_route


def route_overhauled():
    # This route takes heavy inspiration from the unlock order that discord
    # user "legoman12343" posted in the official "The Farmer Was Replaced"
    # discord, it does not include any Unlocks.Dinosaurs or Unlocks.Cactus
    # because we deal with those inside the do_final() function in the
    # timed_run.py file, to get a faster time by pre-buying seeds for both.
    # Also, every unlock ever is here with the price commented out, which
    # makes it easy to tweak the run by moving lines around before the
    # `return route` statement
    route = []

    # In a one by one:
    route.append(Unlocks.Grass)  # 1 requires: {Items.Hay: 100}
    route.append(Unlocks.Speed)  # 1 requires: {Items.Hay: 20}
    route.append(Unlocks.Expand)  # 1 requires: {Items.Hay: 30}

    # In a three by one:
    route.append(Unlocks.Plant)  # 1 requires: {Items.Hay: 50}
    route.append(Unlocks.Expand)  # 2 requires: {Items.Wood: 20}

    # In a three by three:
    route.append(Unlocks.Speed)  # 2 requires: {Items.Wood: 10}
    route.append(Unlocks.Grass)  # 2 requires: {Items.Hay: 300}
    route.append(Unlocks.Carrots)  # 1 requires: {Items.Wood: 100}
    route.append(Unlocks.Trees)  # 1 requires: {Items.Wood: 50, Items.Carrot: 200}
    route.append(Unlocks.Trees)  # 2 requires: {Items.Hay: 300}
    route.append(Unlocks.Expand)  # 3 requires: {Items.Wood: 50, Items.Carrot: 50}

    # In a four by four:
    route.append(Unlocks.Speed)  # 3 requires: {Items.Wood: 50, Items.Carrot: 100}
    route.append(Unlocks.Carrots)  # 2 requires: {Items.Wood: 300}
    route.append(Unlocks.Sunflowers)  # 1 requires: {Items.Carrot: 500}
    route.append(Unlocks.Speed)  # 4 requires: {Items.Wood: 100, Items.Carrot: 200}
    route.append(Unlocks.Grass)  # 3 requires: {Items.Hay: 450}
    route.append(Unlocks.Grass)  # 4 requires: {Items.Hay: 675}
    route.append(Unlocks.Trees)  # 3 requires: {Items.Hay: 480}
    route.append(Unlocks.Trees)  # 4 requires: {Items.Hay: 768}
    route.append(Unlocks.Carrots)  # 3 requires: {Items.Wood: 480}
    route.append(Unlocks.Speed)  # 5 requires: {Items.Carrot: 350}
    route.append(Unlocks.Carrots)  # 4 requires: {Items.Wood: 768}
    route.append(Unlocks.Speed)  # 6 requires: {Items.Carrot: 500}

    # Key unlock: Polyculture (must get pumpkins first)
    route.append(Unlocks.Pumpkins)  # 1 requires: {Items.Wood: 500, Items.Carrot: 1000}
    route.append(Unlocks.Polyculture)  # 1 requires: {Items.Hay: 3000, Items.Wood: 3000, Items.Carrot: 3000}

    # Unlock fertilizer as soon as we unlock pumpkins, to minimize the terrors of the dreaded pumpkin bug:
    route.append(Unlocks.Fertilizer)  # 1 requires: {Items.Pumpkin: 1000}

    route.append(Unlocks.Speed)  # 7 requires: {Items.Carrot: 800}
    route.append(Unlocks.Speed)  # 8 requires: {Items.Carrot: 1100}
    route.append(Unlocks.Carrots)  # 5 requires: {Items.Wood: 1230}
    route.append(Unlocks.Speed)  # 9 requires: {Items.Carrot: 1400}
    route.append(Unlocks.Pumpkins)  # 2 requires: {Items.Carrot: 1200}
    route.append(Unlocks.Pumpkins)  # 3 requires: {Items.Carrot: 1920}
    route.append(Unlocks.Pumpkins)  # 4 requires: {Items.Carrot: 3070}

    # We fast-forward two expand levels
    # In a five by five:
    route.append(Unlocks.Expand)  # 4 requires: {Items.Wood: 100, Items.Pumpkin: 200}

    # In a six by six:
    route.append(Unlocks.Expand)  # 5 requires: {Items.Pumpkin: 500}

    # In a seven by seven:
    route.append(Unlocks.Speed)  # 10 requires: {Items.Carrot: 1700}
    route.append(Unlocks.Carrots)  # 6 requires: {Items.Wood: 1970}
    route.append(Unlocks.Speed)  # 11 requires: {Items.Carrot: 2100}
    route.append(Unlocks.Speed)  # 12 requires: {Items.Carrot: 2500}
    route.append(Unlocks.Trees)  # 5 requires: {Items.Hay: 1230}
    route.append(Unlocks.Pumpkins)  # 5 requires: {Items.Carrot: 4920}
    route.append(Unlocks.Pumpkins)  # 6 requires: {Items.Carrot: 7860}
    route.append(Unlocks.Expand)  # 6 requires: {Items.Pumpkin: 1750}
    route.append(Unlocks.Expand)  # 7 requires: {Items.Pumpkin: 6120}

    # In a eight by eight:
    route.append(Unlocks.Mazes)  # 1 requires: {Items.Carrot: 2000, Items.Pumpkin: 3000}
    route.append(Unlocks.Mazes)  # 2 requires: {Items.Pumpkin: 4000}
    route.append(Unlocks.Mazes)  # 3 requires: {Items.Pumpkin: 8000}
    route.append(Unlocks.Mazes)  # 4 requires: {Items.Pumpkin: 16000}


    return route # Anything below here, we never unlock.

    route.append(Unlocks.Grass)  # 5 requires: {Items.Hay: 1010}
    route.append(Unlocks.Grass)  # 6 requires: {Items.Hay: 1520}
    route.append(Unlocks.Grass)  # 7 requires: {Items.Hay: 2280}
    route.append(Unlocks.Grass)  # 8 requires: {Items.Hay: 3420}
    route.append(Unlocks.Grass)  # 9 requires: {Items.Hay: 5130}
    route.append(Unlocks.Grass)  # 10 requires: {Items.Hay: 7690}
    route.append(Unlocks.Grass)  # 11 requires: {Items.Hay: 11500}
    route.append(Unlocks.Grass)  # 12 requires: {Items.Hay: 17300}

    route.append(Unlocks.Trees)  # 7 requires: {Items.Hay: 3150}
    route.append(Unlocks.Trees)  # 8 requires: {Items.Hay: 5030}
    route.append(Unlocks.Trees)  # 9 requires: {Items.Hay: 8050}
    route.append(Unlocks.Trees)  # 10 requires: {Items.Hay: 12900}
    route.append(Unlocks.Trees)  # 11 requires: {Items.Hay: 20600}
    route.append(Unlocks.Trees)  # 12 requires: {Items.Hay: 33000}

    route.append(Unlocks.Carrots)  # 7 requires: {Items.Wood: 3150}
    route.append(Unlocks.Carrots)  # 8 requires: {Items.Wood: 5030}
    route.append(Unlocks.Carrots)  # 9 requires: {Items.Wood: 8050}
    route.append(Unlocks.Carrots)  # 10 requires: {Items.Wood: 12900}
    route.append(Unlocks.Carrots)  # 11 requires: {Items.Wood: 20600}
    route.append(Unlocks.Carrots)  # 12 requires: {Items.Wood: 33000}

    route.append(Unlocks.Expand)  # 8 requires: {Items.Pumpkin: 21400}
    route.append(Unlocks.Expand)  # 9 requires: {Items.Pumpkin: 75000}

    route.append(Unlocks.Speed)  # 13 requires: {Items.Power: 2000}
    route.append(Unlocks.Speed)  # 14 requires: {Items.Power: 2600}
    route.append(Unlocks.Speed)  # 15 requires: {Items.Power: 3380}
    route.append(Unlocks.Speed)  # 16 requires: {Items.Power: 4390}
    route.append(Unlocks.Speed)  # 17 requires: {Items.Power: 5710}
    route.append(Unlocks.Speed)  # 18 requires: {Items.Power: 7430}
    route.append(Unlocks.Speed)  # 19 requires: {Items.Power: 9650}
    route.append(Unlocks.Speed)  # 20 requires: {Items.Power: 12500}

    route.append(Unlocks.Mazes)  # 5 requires: {Items.Pumpkin: 32000}

    route.append(Unlocks.Pumpkins)  # 7 requires: {Items.Carrot: 12600}
    route.append(Unlocks.Pumpkins)  # 8 requires: {Items.Carrot: 20100}
    route.append(Unlocks.Pumpkins)  # 9 requires: {Items.Carrot: 32200}
    route.append(Unlocks.Pumpkins)  # 10 requires: {Items.Carrot: 51500}

    route.append(Unlocks.Sunflowers)  # 2 requires: {Items.Gold: 1000}
    route.append(Unlocks.Sunflowers)  # 3 requires: {Items.Gold: 2000}
    route.append(Unlocks.Sunflowers)  # 4 requires: {Items.Gold: 4000}
    route.append(Unlocks.Sunflowers)  # 5 requires: {Items.Gold: 8000}
    route.append(Unlocks.Sunflowers)  # 6 requires: {Items.Gold: 16000}

    # All of this is dealt with by the do_final() function in timed_run.py
    route.append(Unlocks.Cactus)  # 1 requires: {Items.Gold: 5000}
    route.append(Unlocks.Cactus)  # 2 requires: {Items.Gold: 10000}
    route.append(Unlocks.Cactus)  # 3 requires: {Items.Gold: 20000}
    route.append(Unlocks.Cactus)  # 4 requires: {Items.Gold: 40000}

    route.append(Unlocks.Dinosaurs)  # 1 requires: {Items.Cactus: 5000}
    route.append(Unlocks.Dinosaurs)  # 2 requires: {Items.Cactus: 1000}
    route.append(Unlocks.Dinosaurs)  # 3 requires: {Items.Cactus: 2000}

    route.append(Unlocks.Leaderboard)  # 1 requires: {Items.Bones: 2000}


def get_me_best_route():
    return route_overhauled()

while True:
    quick_print("° This file should never be run by itself")
