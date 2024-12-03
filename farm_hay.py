def harv_hay_dumb(hay_target):
    for i in range(get_world_size()):
        harvest()
        if get_ground_type() == Grounds.Soil:
            till()
        move(North)

    while num_items(Items.Hay) < hay_target:
        smart_harv()
        move(North)

while True:
    print("This file should be run from Method Tester.py")
