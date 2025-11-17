from navigation import navigate_smart

def wait_harv():
    while not can_harvest():
        if get_entity_type() == None:
            break
    harvest()


def smart_harv(debate=True):
    if can_harvest():
        harvest()
    elif debate:
        try_water()


def try_water(thresh=0.75):
    if get_water() < thresh:
        if num_items(Items.Water) > 0:
            use_item(Items.Water)
        else:
            quick_print("Tried watering, but had no water")


def try_fert():
    if num_unlocked(Unlocks.Fertilizer) == 0:
        return False
    return use_item(Items.Fertilizer)


def time_stamp():
    return get_time()


def ensure_seed(what):
    return get_cost(what)


def spawn_wrapper(task, start_from = None, hat = None):
    # This should be called as the argument of spawn_drone().
    if start_from:
        navigate_smart(start_from)
    if hat:
        change_hat(hat)
    task()

if __name__ == "__main__":
    while True:
        print("° This file should never be run by itself")
