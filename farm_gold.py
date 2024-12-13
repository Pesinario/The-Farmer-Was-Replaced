from navigation import navigate_smart


def enter_a_maze():
    # Get into a maze:
    navigate_smart([0, 0])
    while get_entity_type() != Entities.Hedge:
        if get_entity_type() != Entities.Bush:
            harvest()
            plant(Entities.Bush)
        if num_items(Items.Fertilizer) < 25: # Keep some for pumpkins
            return False
        else:
            use_item(Items.Fertilizer)
    return True


def do_simple_maze_runs(runs_target):
    runs_done = 0
    while runs_done < runs_target:
        if not enter_a_maze():
            quick_print("° Error @do_simple_maze_runs: could not enter maze",
                            "runs done:", runs_done)
            return False
        # Now we should be in a maze.
        dir_list = (East, South, West, North, # I think repeating this
                    East, South, West, North) # will make my logic easier.
        index_last = 0 # represents last successful move
        dir_len = len(dir_list) // 2 # It repeats twice.
        successful_moves = 0

        # Inside the maze loop:
        while get_entity_type() != Entities.Treasure:
            # Getting stuck prevention, I'm not 100% sure if it's needed or
            # not, but it's gotten stuck in earlier versions.
            if successful_moves > 1000:
                quick_print("° Error @do_simple_maze_runs: moves > 1000",
                            "runs done:", runs_done)
                return False

            index_last = index_last % dir_len # index must be < 4.

            if move(dir_list[index_last + 1]):  # if we can turn right, we do it
                index_last += 1
            elif move(dir_list[index_last]):  # if we can go straight, we do it
                pass
            elif move(dir_list[index_last + 3]): # if we can turn left, we do it
                index_last += 3
            elif move(dir_list[index_last + 2]): # go backwards
                index_last += 2
            else: # we should be able to at LEAST move backwards every time.
                successful_moves += 1000
                print("° Terrible error in maze solving logic.")
            successful_moves += 1

        quick_print("- Found Treasure after", successful_moves, "moves")
        harvest()
        runs_done += 1
    return True


while True:
    print("° This file should be run from method_tester.py")
