clear()
tiles = get_world_size()**2
till_this_many_tiles(tiles)
print(tiles)
megaPumpkin = False

while True:
    if megaPumpkin:
        harvest()
        megaPumpkin = False
    acquire_seeds(Items.Pumpkin_Seed, tiles)
    megaPumpkin = True
    for i in range(tiles):
        if get_entity_type() != Entities.Pumpkin:
            plant(Entities.Pumpkin)
            megaPumpkin = False
        debate_watering()
        walk_the_grid()
    do_a_flip()