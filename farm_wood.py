def three_by_three_bush(wood_target):
    # initial setup:
    for next_move in precalc:
        harvest()
        plant(Entities.Bush)
        move(next_move)

    while True:
        if num_items(Items.Wood) > wood_target:
            return True
        for next_move in precalc:
            wait_harv()
            plant(Entities.Bush)
            move(next_move)

def tree_and_bush(wood_target):
    while True:
        for next_move in precalc:
            posSum = get_pos_x()+get_pos_y()
            if posSum % 2 == 0:
                smart_harv(True)
                plant(Entities.Tree)
            else:
                smart_harv(False)
                plant(Entities.Bush)
            move(next_move)
        if num_items(Items.Wood) > wood_target:
            return True

while True:
    print("° This file should be run from Method Tester.py")
