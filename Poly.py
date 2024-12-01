def poly_farm(priority_as_item, target_amount, precalc):
    WORLD_TILE_COUNT = get_world_size()**2
    # ent_to_item = {Entities.Grass:Items.Hay, Entities.Carrots:Items.Carrot, Entities.Tree:Items.Wood}
    item_to_ent = {Items.Hay:Entities.Grass,      # We do not place bushes here since we know we have
                   Items.Carrot:Entities.Carrots, # trees unlocked, also neither sunflowers
                   Items.Wood:Entities.Tree}      # nor pumpkins can be companions
    priority_as_entity = item_to_ent[priority_as_item]
    companion_requests = {}
    till_this_many_tiles(WORLD_TILE_COUNT)
    while True: # Repeating logic
        acquire_seeds(Items.Carrot_Seed, WORLD_TILE_COUNT)

        for next_move in precalc: # Visit every tile once
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
            move(next_move)
        if num_items(priority_as_item) > target_amount: 
            return True

poly_farm(Entities.Grass, 1000, precalc_world) # Default for testing