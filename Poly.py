def poly_farm(priority_as_entity, target_amount, precalc): # TODO: this needs some cleaning up
    WORLD_TILE_COUNT = get_world_size()**2
    ent_to_item = {Entities.Grass:Items.Hay, Entities.Carrots:Items.Carrot, Entities.Tree:Items.Wood} # We do not place bushes here since we know we have trees unlocked, also sunflowers or pumpkins cant be companions
    companion_requests = {}
    till_this_many_tiles(WORLD_TILE_COUNT)
    while True: # Repeating logic
        acquire_seeds(Items.Carrot_Seed, WORLD_TILE_COUNT)

        for i in range(len(precalc)): # Visit every tile once
            current_pos = (get_pos_x(),get_pos_y())
            if current_pos in companion_requests:
                harvest()
                plant(companion_requests.pop(current_pos))
                new_comp = get_companion()
                companion_requests[(new_comp[1], new_comp[2])] = new_comp[0] # I think this is neccesary since we want the key to be a combination of x and y, not the type of plant
                # print(companion_requests)
            else:
                harvest()
                plant(priority_as_entity)
                new_comp = get_companion()
                companion_requests[(new_comp[1], new_comp[2])] = new_comp[0] # I think this is neccesary since we want the key to be a combination of x and y, not the type of plant
                # print("no request")
            move(precalc[i])
        if num_items(ent_to_item[priority_as_entity]) > target_amount: 
            return True
    return False # this is for debugging

# below this line is stuff for debugging kidna

poly_farm(Entities.Grass, 1000)