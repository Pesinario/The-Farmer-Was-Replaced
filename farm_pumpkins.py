from utils import debate_watering, try_fert
from navigation import navigate_smart, precalc


def find_suspects():
    starting_suspects = []
    # Initial setup:
    while get_entity_type() == Entities.Pumpkin and not can_harvest():
        do_a_flip()  # We wait for it to grow, this is for cases where
        # we are so fast that we don't give the first pumpkin planted
        # time to grow, can also happen if the first pumpkin dies.

    for next_move in precalc:
        if get_entity_type() != Entities.Pumpkin:
            if not plant(Entities.Pumpkin):
                quick_print("° Couldn't plant, fatal issue @find_suspects")
                return False

        if not can_harvest():
            debate_watering(0.75)
            starting_suspects.append([get_pos_x(), get_pos_y()])
        move(next_move)
    return starting_suspects


def water_dead(suspects):
    water_counter = 0
    while len(suspects) > 0:
        water_counter += 1
        quick_print("suspects as defined by water_dead at water counter #:", water_counter, suspects)
        local_sus = suspects.pop(0)
        navigate_smart(local_sus)

        if can_harvest():
            continue

        if get_entity_type() != Entities.Pumpkin:
            if not plant(Entities.Pumpkin):
                quick_print("° Couldn't plant, fatal issue @ water_dead")
                return False
            while get_water() <= 0.75:
                debate_watering(0.75)
            suspects.append(local_sus)
    return True


def fert_dead(suspects):
    fert_counter = 0
    while len(suspects) > 0:
        fert_counter += 1
        quick_print("suspects as defined by fert_dead at fert counter #:", fert_counter, suspects)
        current_target = suspects.pop(0)
        navigate_smart(current_target)
        while not can_harvest():
            if get_entity_type() != Entities.Pumpkin:
                if not plant(Entities.Pumpkin):
                    quick_print("° Couldn't plant, fatal issue @ fert_dead")
                    return False
            if not try_fert():
                quick_print("° Can't fert dude!, reverting to water_dead")
                suspects.append(current_target)
                return water_dead(suspects)
    return True


def pumpkin_smart(runs_to_do, run_counter=0):
    while runs_to_do > run_counter:  # Loop for everything
        run_counter += 1
        quick_print("This is pumpkin run N°", run_counter)
        if num_items(Items.Pumpkin_Seed) < (get_world_size()**2):
            quick_print("° Seed issue @ pumpkin_smart, run #:", run_counter)
            return False

        # first planting and watering once run:
        for next_move in precalc:
            harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Pumpkin)  # Don't need to check on this one
            debate_watering(0.25)
            move(next_move)

        # now we take note of all pumpkins that died in the first planting run
        # and also water them after replanting
        suspects = find_suspects()
        quick_print("suspects as defined by find_suspects at run #:", run_counter, suspects)
        # now we replant dead pumpkins and water/fertilizer them until we're done.
        if len(suspects) > 0:
            if num_unlocked(Unlocks.Fertilizer) > 0:
                if not fert_dead(suspects):
                    quick_print("° Error replanting with fertilizer unlocked")
            else:
                if not water_dead(suspects):
                    quick_print(
                        "° Error replanting with fertilizer not yet unlocked")
        # end of run
        old_pumpkins = num_items(Items.Pumpkin)
        while not can_harvest():  # harvest last suspect
            if get_entity_type() != Entities.Pumpkin:
                quick_print("- Last suspect died while last check thingy")
                if not plant(Entities.Pumpkin):
                    quick_print(
                        "° Couldn't plant, fatal issue @pumpkin_smart's final harvest.")
                    return False
            debate_watering(0.75)
            try_fert()
        harvest()
        new_pumpkins = num_items(Items.Pumpkin)
        expected_yield = (
            (get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins)
        )
        actual_yield = new_pumpkins - old_pumpkins
        if actual_yield != expected_yield:
            quick_print("° Expected yield was: ", expected_yield, " pumpkins")
            quick_print("° We have farmed ", actual_yield, " pumpkins.")
            quick_print("° We farmed ", expected_yield - actual_yield, " less pumpkins than expected")
            quick_print("° Seeds left:", num_items(Items.Pumpkin_Seed), "run #:", run_counter)
            quick_print("° Fertilizer unlocked?", 1 == num_unlocked(Unlocks.Fertilizer))
            return False
    return True


while True:
    quick_print("° This file should be run from method_tester.py")
