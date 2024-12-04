def find_suspects(precalc):
    starting_suspects = []
    for next_move in precalc:
        if get_entity_type() != Entities.Pumpkin:
            plant(Entities.Pumpkin)
            starting_suspects.append([get_pos_x(), get_pos_y()])
        elif not can_harvest():
            do_a_flip() # wait for growth kinda
        debate_watering(0.25)
        move(next_move)
    return starting_suspects

def water_dead(suspects):
    while len(suspects) > 0:
        local_sus = suspects.pop()
        navigate_smart(local_sus)
        if not can_harvest():
            if not plant(Entities.Pumpkin):
                    print("Couldn't plant, fatal issue @ water_dead")
                    return False
            while get_water() <= 0.75:
                debate_watering(0.75)
            suspects.append(local_sus)
        else:
            quick_print("removing suspect", local_sus)
    return True

def fert_dead(suspects):
    while len(suspects) > 0:
        current_target = suspects.pop()
        navigate_smart(current_target)
        # print("Currently at a suspect", current_target)
        while not can_harvest():
            if get_entity_type() != Entities.Pumpkin:
                if not plant(Entities.Pumpkin):
                    print("Couldn't plant, fatal issue @ fert_dead")
                    return False
            if not try_fert():
                print("Can't fert dude!, will wait")


def pumpkin_smart(pumpkin_target):
    while True: # Loop for everything
        if num_items(Items.Pumpkin_Seed) < get_world_size()**2:
            print("Seed issue @ pumpkin_smart")
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
        debug_counter = 0
        while len(suspects) > 0:
            debug_counter += 1
            if num_unlocked(Unlocks.Fertilizer) > 0:
                fert_dead(suspects)
            else:
                water_dead(suspects)
        if debug_counter > 1:
            quick_print(debug_counter)
        # end of run
        quick_print("We think we found all dead pumpkins")
        old_pumpkins = num_items(Items.Pumpkin)
        harvest()
        new_pumpkins = num_items(Items.Pumpkin)
        expected_yield = (get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins)
        actual_yield = new_pumpkins - old_pumpkins
        if actual_yield != expected_yield: # TODO: clean up all of the debugging stuff eventually
            print("Expected yield was: ", expected_yield, " pumpkins")
            print("We have farmed ", actual_yield, " pumpkins.")
            print("We farmed ", expected_yield - actual_yield, " less pumpkins than expected")
        if num_items(Items.Pumpkin) > pumpkin_target:
            return True

while True:
    print("This file should be run from Method Tester.py")
