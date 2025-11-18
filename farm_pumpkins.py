from utils import try_water, try_fert
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
            try_water(0.75)
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
                try_water(0.75)
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


def plant_field():
    for y in range(get_world_size()):
        navigate_smart((0, y))
        def task(hat=Hats.Pumpkin_Hat):
            change_hat(hat)
            for _ in range(get_world_size()):
                harvest()
                if get_ground_type() != Grounds.Soil:
                    till()
                plant(Entities.Pumpkin)
                try_water()
                move(East)

        if not spawn_drone(task):
            task(Hats.Wizard_Hat)


def fix_row(row):
    navigate_smart((0, row))
    def task(hat=Hats.Pumpkin_Hat):
        change_hat(hat)
        for _ in range(get_world_size()):
            while not can_harvest():
                if get_entity_type() != Entities.Pumpkin:
                    plant(Entities.Pumpkin)
                    if not try_fert():
                        print("° Could not fertilize at ",get_pos_x(), ", ", get_pos_y()," !!!!")
                        break
            move(East)

    if not spawn_drone(task):
        task(Hats.Wizard_Hat)


def pumpkin_multi(runs_to_do, run_counter=0):
    while runs_to_do > run_counter:  # Loop for everything
        run_counter += 1
        plant_field()
        for _ in range(get_world_size()):
            fix_row(_)

        # end of run
        old_pumpkins = num_items(Items.Pumpkin)
        old_weird = num_items(Items.Weird_Substance)
        while not can_harvest():  # harvest last suspect
            if get_entity_type() != Entities.Pumpkin:
                quick_print("- Last suspect died while last check thingy")
                if not plant(Entities.Pumpkin):
                    quick_print(
                        "° Couldn't plant, fatal issue @pumpkin_smart's final harvest.")
                    return False
            try_water(0.75)
            try_fert()

        while num_drones() > 1:
            do_a_flip()

        harvest()
        new_pumpkins = num_items(Items.Pumpkin)
        new_weird = num_items(Items.Weird_Substance)
        pumpkin_yield = new_pumpkins - old_pumpkins
        weird_yield = new_weird - old_weird

        if get_world_size() > 6:
            expected_yield = 6 * get_world_size() ** 2
        else:
            expected_yield = get_world_size() ** 3
        expected_yield *= 2 ** (num_unlocked(Unlocks.Pumpkins) - 1)  # Upgrades

        if weird_yield + pumpkin_yield != expected_yield:
            quick_print("° Expected yield was: ", expected_yield, " pumpkins")
            quick_print("° We have farmed ", pumpkin_yield, " pumpkins and ", weird_yield, "weird substance")
            quick_print("° Fertilizer unlocked?", 1 == num_unlocked(Unlocks.Fertilizer))
            return False
    return True


def pumpkin_smart(runs_to_do, run_counter=0):
    while runs_to_do > run_counter:  # Loop for everything
        run_counter += 1
        #quick_print("This is pumpkin run N°", run_counter)
        #if num_items(Items.Pumpkin_Seed) < (get_world_size()**2):
        #    quick_print("° Seed issue @ pumpkin_smart, run #:", run_counter)
        #    return False

        # first planting and watering once run:
        for next_move in precalc:
            harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Pumpkin)  # Don't need to check on this one
            try_water(0.25)
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
        old_weird = num_items(Items.Weird_Substance)
        while not can_harvest():  # harvest last suspect
            if get_entity_type() != Entities.Pumpkin:
                quick_print("- Last suspect died while last check thingy")
                if not plant(Entities.Pumpkin):
                    quick_print(
                        "° Couldn't plant, fatal issue @pumpkin_smart's final harvest.")
                    return False
            try_water(0.75)
            try_fert()
        harvest()
        new_pumpkins = num_items(Items.Pumpkin)
        new_weird = num_items(Items.Weird_Substance)
        pumpkin_yield = new_pumpkins - old_pumpkins
        weird_yield = new_weird - old_weird

        if get_world_size() > 6:
            expected_yield = 6 * get_world_size() ** 2
        else:
            expected_yield = get_world_size() ** 3
        expected_yield *= 2 ** (num_unlocked(Unlocks.Pumpkins) - 1)  # Upgrades

        if weird_yield + pumpkin_yield != expected_yield:
            quick_print("° Expected yield was: ", expected_yield, " pumpkins")
            quick_print("° We have farmed ", pumpkin_yield, " pumpkins and ", weird_yield, "weird substance")
            quick_print("° Fertilizer unlocked?", 1 == num_unlocked(Unlocks.Fertilizer))
            return False
    return True


if __name__ == "__main__":
    while True:
        print("° This file should be run from method_tester.py")
