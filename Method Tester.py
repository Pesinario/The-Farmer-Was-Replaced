OPTIMAL_PUMPKIN_SEEDS = {2:17, 3:27, 4:40, 5:55,
                         6:72, 7:92, 8:115, 9:140} # Do not even ask where these numbers came from
ORDER_OF_GRIND = [
    Items.Egg, Items.Cactus, Items.Gold,Items.Pumpkin, Items.Pumpkin,
    Items.Power, Items.Carrot, Items.Wood, Items.Hay]
EXPECTED_POWER = {2:18.31, 3:46.97, 4:73.63, 5:126.14,
                  6:191.86, 7:281.47, 8:397.77, 9:544.71}

clear()
set_farm_size(3)
set_execution_speed(3)

precalc = precalc_world()


# To use or test any of the grinding functions, remove the "#"
WANTED_AMOUNT = 600 # This is how much MORE than you currently have you want
default_poly = Items.Carrot

# grind_method(Items.Bones, num_items(Items.Bones) + 2000)

# Hay:
#harv_hay_dumb(num_items(Items.Hay) + WANTED_AMOUNT)
#hay_full_field(num_items(Items.Hay) + WANTED_AMOUNT)

# Wood:
#one_by_three_bush_hay_wait(num_items(Items.Wood) + WANTED_AMOUNT)
#three_by_three_bush(num_items(Items.Wood) + WANTED_AMOUNT)
#three_by_three_with_hay(num_items(Items.Wood) + WANTED_AMOUNT)
#tree_and_bush(num_items(Items.Wood) + WANTED_AMOUNT)

# Carrots:
#carrots_ensure_seeds(num_items(Items.Carrot) + WANTED_AMOUNT)
#carrot_three_by_three(num_items(Items.Carrot) + WANTED_AMOUNT)
#carrots_trusting(num_items(Items.Carrot) + WANTED_AMOUNT)

# Polyculture (Choose what to prioritize):
#poly_farm(default_poly, num_items(default_poly) + WANTED_AMOUNT)

# Pumpkins:
#pumpkin_smart(num_items(Items.Pumpkin) + WANTED_AMOUNT)

# Power:
#old_method_sunflower(num_items(Items.Power) + WANTED_AMOUNT)
#get_power(num_items(Items.Power) + WANTED_AMOUNT)

# Gold:
#do_simple_maze_run(num_items(Items.Gold) + WANTED_AMOUNT)

# Cactus:
#cactus_bubble(num_items(Items.Cactus) + WANTED_AMOUNT)

# Bones:
#ultra_dumb_dyno(num_items(Items.Bones) + WANTED_AMOUNT)
#dyno_slightly_smarter(num_items(Items.Bones) + WANTED_AMOUNT)
