from navigation import walk_the_grid, precalc
from utils import smart_harv
from resource_management import acquire_seeds


def ultra_dumb_dyno(bones_target):  # This farming method is deprecated
    WORLD_TILE_COUNT = get_world_size()**2
    while True:
        if num_items(Items.Egg) < WORLD_TILE_COUNT:
            for _ in range(WORLD_TILE_COUNT):
                smart_harv(False)
                walk_the_grid()
            if not acquire_seeds(Items.Egg, WORLD_TILE_COUNT):
                quick_print("° We're broke! This was a terrible idea!")
        for _ in range(WORLD_TILE_COUNT):
            smart_harv(False)
            use_item(Items.Egg)
            walk_the_grid()
        if num_items(Items.Bones) > bones_target:
            return True


# Still nowhere near optimal, but much better.
def dyno_slightly_smarter(bones_target):
    while num_items(Items.Bones) < bones_target:
        for next_move in precalc:
            if get_entity_type() != Entities.Dinosaur:
                use_item(Items.Egg)
            count = 0
            here = measure()
            west = measure(West)
            east = measure(East)
            north = measure(North)
            south = measure(South)
            dyno_here = here != None
            if dyno_here and here == west:
                count += 1
            if dyno_here and here == north:
                count += 1
            if dyno_here and here == east:
                count += 1
            if dyno_here and here == south:
                count += 1

            if count > 2: # Risky, but may work.
                harvest()
                use_item(Items.Egg)

            if dyno_here and west != None and here < west:
                swap(West)
            # if here != None and north != None and here < north:
            #     swap(North)
            if dyno_here and east != None and here > east:
                swap(East)
            # if here != None and south != None and here > south:
            #     swap(South)
            move(next_move)
    return True


while True:
    quick_print("° This file should be run from method_tester.py")
