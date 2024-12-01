while True:
    clear()
    plant(Entities.Bush)
    trade(Items.Fertilizer)
    while not get_entity_type() == Entities.Hedge:
        try_fert()
    # Now we should be in a maze.
    dir_list = [East, North, West, South]
    last_dir = 0
    last_ok = True
    while get_entity_type() != Entities.Treasure:
        dir_index = random() * len(dir_list) // 1
        move(dir_list[dir_index])
    harvest()
    print("Wow, this worked lmao")
