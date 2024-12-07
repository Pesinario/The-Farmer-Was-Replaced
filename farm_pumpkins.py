def find_suspects(precalc):
    starting_suspects = []
    count = 0
    for next_move in precalc:
        if count == 0:
            if get_entity_type() != Entities.Pumpkin:
                plant(Entities.Pumpkin)
            while get_entity_type() == Entities.Pumpkin and not can_harvest():
                do_a_flip() # We wait for it to grow, this is for cases where
                # we are so fast that we don't give the first pumpkin planted
                # time to grow

        if get_entity_type() != Entities.Pumpkin:
            plant(Entities.Pumpkin)
            starting_suspects.append([get_pos_x(), get_pos_y()])
        elif not can_harvest():
            debate_watering(0.75)
        move(next_move)
        count += 1
    return starting_suspects

def water_dead(suspects):
    while len(suspects) > 0:
        local_sus = suspects.pop(0)
        navigate_smart(local_sus)

        if can_harvest():
            continue

        if get_entity_type() != Entities.Pumpkin:
            if not plant(Entities.Pumpkin):
                print("° Couldn't plant, fatal issue @ water_dead")
                return False
            while get_water() <= 0.75:
                debate_watering(0.75)
            suspects.append(local_sus)
    return True

def fert_dead(suspects):
    while len(suspects) > 0:
        current_target = suspects.pop(0)
        navigate_smart(current_target)
        while not can_harvest():
            if get_entity_type() != Entities.Pumpkin:
                if not plant(Entities.Pumpkin):
                    print("° Couldn't plant, fatal issue @ fert_dead")
                    return False
            if not try_fert():
                quick_print("° Can't fert dude!, reverting to water_dead")
                suspects.append(current_target)
                return water_dead(suspects)
    return True


def pumpkin_smart(pumpkin_target):
    while True: # Loop for everything
        if num_items(Items.Pumpkin) > pumpkin_target:
            return True
        elif num_items(Items.Pumpkin_Seed) < (get_world_size()**2):
            print("° Seed issue @ pumpkin_smart")
            return False

        # first planting and watering once run:
        for next_move in precalc:
            harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Pumpkin)
            debate_watering(0.25)
            move(next_move)

        # now we take note of all pumpkins that died in the first planting run
        suspects = find_suspects(precalc)

        # now we replant dead pumpkins untill we're sure that all pumpkins are alive
        if len(suspects) > 0:
            if num_unlocked(Unlocks.Fertilizer) > 0:
                fert_dead(suspects)
            else:
                water_dead(suspects)
        # end of run
        old_pumpkins = num_items(Items.Pumpkin)
        smart_harv()
        new_pumpkins = num_items(Items.Pumpkin)
        expected_yield = (get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins)
        actual_yield = new_pumpkins - old_pumpkins
        if actual_yield != expected_yield: # TODO: clean up all of the debugging stuff eventually
            print("° Expected yield was: ", expected_yield, " pumpkins")
            print("° We have farmed ", actual_yield, " pumpkins.")
            print("° We farmed ", expected_yield - actual_yield, " less pumpkins than expected")


while True:
    print("° This file should be run from Method Tester.py")
