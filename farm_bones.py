#"""#This module contains bone farming methods.#"""#
from navigation import walk_the_grid, precalc
from utils import smart_harv
from resource_managment import acquire_seeds

def ultra_dumb_dyno(bones_target): # This farming method is deprecated
    WORLD_TILE_COUNT = get_world_size()**2
    while True:
        if num_items(Items.Egg) < WORLD_TILE_COUNT:
            for _ in range(WORLD_TILE_COUNT):
                smart_harv(False)
                walk_the_grid()
            if not acquire_seeds(Items.Egg, WORLD_TILE_COUNT):
                print("° We're broke! This was a terrible idea!")
        for _ in range(WORLD_TILE_COUNT):
            smart_harv(False)
            use_item(Items.Egg)
            walk_the_grid()
        if num_items(Items.Bones) > bones_target:
            return True


def dyno_slightly_smarter(bones_target): # Still nowhere near optimal, but much better.
    while num_items(Items.Bones) < bones_target:
        if num_items(Items.Egg) == 0:
            quick_print("° Egg issue @ dyno_slightly_smarter()")
            return False

        for next_move in precalc:
            if get_entity_type() != Entities.Dinosaur:
                use_item(Items.Egg)
            count = 0
            here = measure()
            west = measure(West)
            east = measure(East)
            north = measure(North)
            south = measure(South)

            if here != None and west != None and here == west:
                count += 1
            if here != None and north != None and here == north:
                count += 1
            if here != None and east != None and here == east:
                count += 1
            if here != None and south != None and here == south:
                count += 1

            if count > 3:
                harvest()
                use_item(Items.Egg)

            if here != None and west != None and here < west:
                swap(West)
            # if here != None and north != None and here < north:
            #     swap(North)
            if here != None and east != None and here > east:
                swap(East)
            # if here != None and south != None and here > south:
            #     swap(South)
            move(next_move)
    return True

while True:
    print("° This file should be run from Method Tester.py")
