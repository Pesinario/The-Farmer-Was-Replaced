from navigation import navigate_dumb

def prepare_dinosaurs():
    clear()
    change_hat(Hats.Dinosaur_Hat)


def snake_basic(target_bones):
    apple = measure()
    while num_items(Items.Bone) < target_bones:
        if not navigate_dumb(apple[0], apple[1]):
            return False
        apple = measure()
    return True


def snake_fill_farm(runs):
    l = get_world_size()
    move(East)
    while runs > 0:
        runs -= 1
        for _ in range(l):
            if get_pos_y() % 2 == 0:
                for _ in range(l - 2):
                    move(East)
            else:
                for _ in range(l - 2):
                    move(West)
            move(North)
        move(West)
        for _ in range(l):
            move(South)
        move(East)


if __name__ == "__main__":
    while True:
        print("° This file should be run from method_tester.py")
