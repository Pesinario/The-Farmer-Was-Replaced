from navigation import navigate_smart, navigate_dumb


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
                quick_print("° Terrible error in maze solving logic.")
            successful_moves += 1

        quick_print("- Found Treasure after", successful_moves, "moves")
        harvest()
        runs_done += 1
    return True


# Some blind methods for maze_brach_based:


def list_visited():
    # First, we do a simple right hand rule run of the maze, but we keep track
    # of the moves we made and we don't stop if we found treasure.
    MAX_SEARCH_LENGTH = get_world_size() ** 2
    STARTED_AT = (get_pos_x(), get_pos_y())
    dir_list = (East, South, West, North, # I think repeating this
                East, South, West, North) # will make my logic easier.
    index_last = 0 # represents last successful move
    dir_len = len(dir_list) // 2 # It repeats twice.
    positions_visited = []
    successful_moves = 0
    treasure_loc = None

    while True:
        curr_loc = (get_pos_x(), get_pos_y())
        if get_entity_type() == Entities.Treasure:
            treasure_loc = curr_loc
        positions_visited.append(curr_loc)

        if curr_loc == STARTED_AT:
            if len(set(positions_visited)) == MAX_SEARCH_LENGTH:
                break

        if successful_moves > 1000: # in case the maze has islands.
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
            quick_print("° Terrible error in maze solving logic.")
        successful_moves += 1
    return positions_visited, treasure_loc


def climb_up_branch(climb_this_branch, my_pos_index = None):
    # gets me to the start of the branch
    quick_print("climb_up_branch called with",climb_this_branch)

    if my_pos_index == None:
        my_coords = (get_pos_x(), get_pos_y())
        index = 0
        for pos in climb_this_branch:
            if pos == my_coords:
                my_pos_index = index
                break
            index += 1

    while my_pos_index > 0:
        my_pos_index -= 1
        navigate_dumb(
            climb_this_branch[my_pos_index][0],
            climb_this_branch[my_pos_index][1]
            )


def climb_down_branch(climb_this_branch):
    # get me to the end of the branch
    quick_print("climb_down_branch called with",climb_this_branch)
    my_pos_index = 0
    branch_stop = len(climb_this_branch) - 1
    while my_pos_index < branch_stop:
        my_pos_index += 1
        navigate_dumb(
            climb_this_branch[my_pos_index][0],
            climb_this_branch[my_pos_index][1]
            )


def find_treasure_in_branch(branch, curr_index, change):
    quick_print("@find_treasure_in_branch was called on branch", branch)
    quick_print("with index:", curr_index, "and change:", change)
    while get_entity_type() != Entities.Treasure:
        navigate_dumb(branch[curr_index][0], branch[curr_index][1])
        curr_index += change


def maze_branch_based(runs_target):
    # First, we enter our maze:
    if not enter_a_maze():
        quick_print("° Error @maze_reusing: could not enter maze")
        return False

    # Then, we try record maze data
    output = list_visited()
    if output == False:
        quick_print("° Error learning the maze @maze_reusing.")
        return False
    history, treasure_location = output

    # Now we define a bunch of functions, and interpret the maze data:
    def find_nodes(history):
        queue = list(history)
        my_nodes = set()
        while len(queue) > 0:
            curr_pos = queue.pop()
            count = 1
            while curr_pos in queue:
                count += 1
                queue.remove(curr_pos)
            if count > 2:
                my_nodes.add(curr_pos)
        return my_nodes


    nodes = find_nodes(history)
    quick_print("nodes", nodes)

    def pruned_branches_no_dupes(history):
        def find_branches(list_of_positions):
            def prune_current(branch):
                pruned = []
                for item in branch:
                    if item not in pruned:
                        pruned.append(item)
                    else:
                        return pruned
                return pruned
            work_branches = []
            current_branch = []
            for pos in list_of_positions:
                if pos in nodes: # We either backtracked or about to split into different branches.
                    current_branch.append(pos)
                    work_branches.append(prune_current(current_branch)) # we prune for the
                    # scenario that we backtracked.
                    # This is now the NEXT working branch
                    current_branch = []
                    current_branch.append(pos)
                else:
                    current_branch.append(pos)
            return work_branches
        my_branches = find_branches(history)
        my_known_branches = []
        my_known_branches_as_sets = []
        for branch in my_branches:
            branch_set = set(branch)
            if branch_set in my_known_branches_as_sets:
                continue
            else:
                my_known_branches_as_sets.append(branch_set)
                my_known_branches.append(branch)
        return my_known_branches


    branches = pruned_branches_no_dupes(history)
    quick_print("branches", branches)

    def map_node_to_child_and_parent():
        nodes_to_children = {}
        for node in nodes: # init placeholders
            nodes_to_children[node]=[]
        nodes_to_parents = {}
        branch_index = 0
        for branch in branches:
            if branch[-1] in nodes:
                nodes_to_parents[branch[-1]] = branch_index
            if len(branch) > 1:
                start = branch[0]
                if start in nodes:
                    stash = nodes_to_children[start]
                    stash.append(branch_index)
                    nodes_to_children[start] = stash
            branch_index += 1
        return nodes_to_children, nodes_to_parents


    node_to_children, node_to_parent = map_node_to_child_and_parent()


    def map_pos_to_branch():
        location_to_branch={}
        world_size = get_world_size()
        for x in range(world_size):
            for y in range(world_size):
                if (x, y) in nodes:
                    is_part_of = node_to_parent[(x, y)]
                    location_to_branch[(x,y)] = is_part_of
                else:
                    branch_index = 0
                    for branch in branches:
                        if (x, y) in branch:
                            is_part_of = branch_index
                            break
                        branch_index += 1
                    location_to_branch[(x,y)] = is_part_of
        return location_to_branch


    pos_to_branch = map_pos_to_branch()


    def find_root():
        branch_index = 0
        for branch in branches:
            if branch[0] not in nodes or len(branch) == 1:
                quick_print(branch_index, "is the first branch:", branch)
                return branch_index
            branch_index += 1


    root_branch = find_root()
    root_node = branches[root_branch][-1]
    quick_print("root_branch", root_branch)
    quick_print("root_node", root_node)

    # the following code has been commented out because it's not used.
    # but I may regret deleting it so i'll just keep it.
#    def find_branch_depth():
#        branch_depth = {root_branch:0}
#        start_pos = branches[root_branch][-1]
#        branch_index = 0
#        for branch in branches:
#            if branch == branches[root_branch]:
#                continue
#            depth_index = 1
#            my_branch_index = branch_index
#            while branches[my_branch_index][0] != start_pos:
#                my_branch_index = node_parents[branches[my_branch_index][0]]
#                depth_index += 1
#            branch_depth[branch_index] = depth_index
#            branch_index += 1
#        return branch_depth
#
#    branch_to_depth = find_branch_depth()


    def find_parents_of_branches():
        parents = {}
        index = 0
        for branch in branches:
            parents[index] = branch[0]
            index += 1
        return parents

    branch_to_parent_node = find_parents_of_branches()


    def get_to_ancestor_smarter(start_index, treasure_index):
        # Before we call this function, we should be at the start of a branch.
        quick_print(get_pos_x(), get_pos_y(), "@get_to_ancestor_smarter")
        def find_last_common_ancestor(a_ancestors, b_ancestors):
            last_ancestor = root_node

            for ancestor in a_ancestors:
                if ancestor not in b_ancestors:
                    return last_ancestor
                else:
                    last_ancestor = ancestor
            return a_ancestors[0] # This happens if a ⊂: b

        def find_ancestors(branch_index):
            # This is it's own function because we do want all the ancestors
            # from the treasure branch
            ancestors = []
            if branch_index == root_branch:
                return [root_node]
            while True:
                curr_ancestor = branch_to_parent_node[branch_index]
                ancestors.append(curr_ancestor)
                if ancestors[-1] == root_node:
                    break
                else: # travel one node up, and add it to ancestors
                    branch_index = node_to_parent[curr_ancestor]

            return ancestors


        my_ancestors = find_ancestors(start_index)
        quick_print("my_ancestors",my_ancestors)
        treasure_ancestors = find_ancestors(treasure_index)
        quick_print("treasure_ancestors",treasure_ancestors)
        last_common_ancestor = find_last_common_ancestor(my_ancestors, treasure_ancestors)
        quick_print("last_common_ancestor",last_common_ancestor)

        my_coords = (get_pos_x(), get_pos_y())
        while my_coords != last_common_ancestor:
            climb_up_branch(
                branches[pos_to_branch[my_coords]],
                len(branches[pos_to_branch[my_coords]]) - 1
                )
            my_coords = (get_pos_x(), get_pos_y())
        # now we are at the latest common ancestor between us and the treasure
        quick_print("We are at most common ancestor",(get_pos_x(),get_pos_y()))

        while treasure_ancestors[-1] != my_coords:
            treasure_ancestors.pop()

        while len(treasure_ancestors) > 0:
            ancestor = treasure_ancestors.pop()
            quick_print("curr ancestor", ancestor)
            for child in node_to_children[ancestor]:
                quick_print("curr child", child, branches[child])
                if branches[child][-1] in treasure_ancestors:
                    quick_print(branches[child][-1], "in treasure_ancestors")
                    climb_down_branch(branches[child])
                    break
                quick_print("child not in ancestors")
        # now we are at the start of the branch that contains treasure.


    def go_to_treasure(treasure_coords):
        # TODO: Consider going greedy and attempting to just walk straight to the treasure
        quick_print("@go_to_treasure was called with treasure_coords", treasure_coords)
        my_coords=(get_pos_x(), get_pos_y())
        treasure_branch_index = pos_to_branch[treasure_coords]
        current_branch_index = pos_to_branch[(get_pos_x(), get_pos_y())]
        my_branch = branches[current_branch_index]

        if current_branch_index == treasure_branch_index:
            quick_print("@go_to_treasure thinks we're on the target branch right of the bat")
            index = 0
            for pos in my_branch:
                if pos == my_coords:
                    my_pos_index = index
                if pos == treasure_coords:
                    treasure_index = index
                index += 1
            if my_pos_index > treasure_index: #pylint:disable=E0606
                change = -1
            else:
                change = 1
            quick_print("my_pos_index", my_pos_index,
                        "treasure_index", treasure_index,
                        "change", change)
            find_treasure_in_branch(my_branch, my_pos_index, change)
            return True
        else:
            quick_print("@go_to_treasure thinks we're NOT on the target branch")
            # get to start of MY branch / next branch if we are at root
            if my_branch == branches[root_branch]:
                quick_print("climbing down root branch")
                climb_down_branch(my_branch)
            else:
                quick_print("climbing up", my_branch, "from within go_to_treasure")
                climb_up_branch(my_branch)
            # get to start of target's branch
            quick_print("about to call get_to_ancestor_smarter")
            get_to_ancestor_smarter(current_branch_index, treasure_branch_index)
            quick_print("we already called get_to_ancestor_smarter")
            find_treasure_in_branch(branches[treasure_branch_index], 0, 1)
            return True

    quick_print(
        "maze_branch_based called for", runs_target, "runs",
        "with", num_items(Items.Fertilizer), "fertilizer available"
        )
    # Finally: We solve mazes until we reach our maze count goal.
    runs_done = 0
    if runs_target > 299: # Just in case
        quick_print("° Asked for more runs than physically possible.")
        runs_target = 299
    while runs_done < runs_target:
        go_to_treasure(treasure_location)
        treasure_location = measure()
        while get_entity_type() == Entities.Treasure:
            # We don't actually use fertilizer if it doesn't work, huh
            if num_items(Items.Fertilizer) < 1:
                quick_print(
                    "° Error @maze_branch_based,",
                    "ran out of fertilizer in run #", runs_done + 1)
                harvest()
                return False
            use_item(Items.Fertilizer)
        runs_done += 1
    go_to_treasure(treasure_location)
    harvest()
    quick_print("- We did", runs_done, "@maze_branch_based")
    return True


while True:
    quick_print("° This file should be run from method_tester.py")
