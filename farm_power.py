from utils import try_water, wait_harv
from navigation import navigate_smart, precalc


def sunflower_no_replanting(should_till):
    my_record = {}

    for next_move in precalc:  # Initial setting up
        if should_till:
            harvest()
            if get_ground_type() != Grounds.Soil:
                till()
        try_water(0.5)
        plant(Entities.Sunflower)
        petals = measure()
        if petals in my_record:  # If other sunflowers have the same number of petals
            petal_siblings = my_record.pop(petals)
            petal_siblings.append([get_pos_x(), get_pos_y()])
            my_record[petals] = petal_siblings
        elif petals == None:
            quick_print("° Some kind of error @ Sunflower Master")
        else:  # First sunflower with that number of petals
            my_record[petals] = [[get_pos_x(), get_pos_y()]]
        move(next_move)

    for i in range(9):  # harvest
        hunting_size = 15 - i
        if hunting_size in my_record:
            siblings = my_record[hunting_size]
            for sunflower in siblings:
                navigate_smart(sunflower)
                wait_harv()


def get_power(power_target=0, need_tilling=True):
    WORLD_TILE_COUNT = get_world_size()**2
    expected_yield = WORLD_TILE_COUNT * 10 + (WORLD_TILE_COUNT - 10) * 5
    runs_to_fulfil = (power_target + 50) // expected_yield

    for _ in range(runs_to_fulfil + 1):
        if WORLD_TILE_COUNT * get_cost(Entities.Sunflower)[Items.Carrot] > num_items(Items.Carrot):
            quick_print("° Seed issue @ get_power")
            return False
        if need_tilling:
            change_hat(Hats.Sunflower_Hat)  # ;)
            sunflower_no_replanting(True)
            need_tilling = False
        else:
            sunflower_no_replanting(False)
    if num_items(Items.Power) < power_target + 40:
        quick_print("° We farmed fewer sunflowers than we needed to.")
        return False
    return True


if __name__ == "__main__":
    while True:
        print("° This file should be run from method_tester.py")
