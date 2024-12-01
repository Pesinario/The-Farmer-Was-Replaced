# WORLD_TILE_COUNT = get_world_size()**2
# till_this_many_tiles(WORLD_TILE_COUNT)
# print(WORLD_TILE_COUNT)

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

# def water_dead(suspects): # TODO: implement this again eventually
#     new_sus = []
#     for i in range(len(suspects)):
#         current_target = suspects[i]
#         navigate_smart(current_target)
#         if not can_harvest():
#             new_sus.append([current_target[0],current_target[1]])
#             if not plant(Entities.Pumpkin):
#                 acquire_seeds(Items.Pumpkin_Seed, (world_tile_count*5 // 1))
#                 plant(Entities.Pumpkin)
#             while get_water() < 0.75:
#                 debate_watering(0.75)
#     print (new_sus)
#     return new_sus

def fert_dead(suspects):
    while len(suspects) > 0:
        current_target = suspects.pop()
        navigate_smart(current_target)
        # print("Currently at a suspect", current_target)
        while not can_harvest():
            if get_entity_type() != Entities.Pumpkin:
                if not plant(Entities.Pumpkin):
                    acquire_seeds(Items.Pumpkin_Seed, ((get_world_size()**2 *5) // 1))
                    plant(Entities.Pumpkin)
            if not try_fert():
                print("Can't fert dude!, will wait")


def pumpkin_smart(pumpkin_target):
    # initial setup:
    while True: # Loop for everything
        if num_items(Items.Pumpkin_Seed < get_world_size()):
            print("Seed issue @ pumpkin_smart")
            return False
        # first planting and watering once run:
        for next_move in precalc: # This is kinda hardcoded, initial run setup
            harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Pumpkin)
            debate_watering(0.25)
            move(next_move)
        # now we try to do mid-run stuff
        suspects = find_suspects(precalc)
        # while len(suspects) > 2:
        #     suspects = water_dead(suspects)
        fert_dead(suspects)
        # end of run
        print("We think we found all dead pumpkins")
        old_pumpkins = num_items(Items.Pumpkin)
        navigate_to(0, 0)
        harvest()
        new_pumpkins = num_items(Items.Pumpkin)
        expected_yield = (get_world_size() ** 3) * num_unlocked(Unlocks.Pumpkins)
        actual_yield = new_pumpkins - old_pumpkins
        if actual_yield != expected_yield: # TODO: clean up all of the debugging stuff eventually
            print("Expected yield was: ", expected_yield, " pumpkins")
            print("We have farmed ", actual_yield, " pumpkins.")
            print("We farmed ", expected_yield - actual_yield, " less pumpkins than expected")
        if num_items(Items.Pumpkin) > pumpkin_target:
            break
# if you wish to run this standalone instead of via timed_run.py, remove the "# "
# precalc = precalc_world()
# pumpkin_smart(num_items(Items.Pumpkin) + 10000)