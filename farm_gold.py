def do_simple_maze_run(gold_target):
    clear() # the farm reverts to grass anyways after harvesting the treasure
    dir_list = [East, South, West, North]
    dir_last = 0
    dir_next = 1
    while True:
        counter = 0
        while not get_entity_type() == Entities.Hedge:
            plant(Entities.Bush)
            try_fert()
        # Now we should be in a maze.
        move(East)
        while get_entity_type() != Entities.Treasure: # solve the maze
            if counter > 1000:
                break
            dir_next = dir_last + 1
            if dir_next > len(dir_list)-1:
                dir_next = 0

            if move(dir_list[dir_next]): # if we can turn right, we do it
                dir_last = dir_next
                continue
            elif move(dir_list[dir_last]): # if we can go straight, we do it
                continue
            else: # we try what would be left from last succesful move
                dir_last += 2
                if dir_last > len(dir_list)-1:
                    dir_last -= len(dir_list)

        harvest()
        if num_items(Items.Gold) > gold_target:
            return True

while True:
    print("This file should be run from Method Tester.py")
