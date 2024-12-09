ORDER_OF_GRIND = [
    Items.Egg, Items.Cactus, Items.Gold,Items.Pumpkin, Items.Pumpkin,
    Items.Power, Items.Carrot, Items.Wood, Items.Hay]

clear()
# set_farm_size(7)
# set_execution_speed(10)

precalc = precalc_world()


# To use or test any of the grinding functions, remove the "#"
WANTED_AMOUNT = 100000 # This is how much MORE than you currently have you want
default_poly = Items.Carrot
grind_target = Items.Gold

# The third parameter in grind_method is whether or not to get power first.
# The fourth parameter in grind_method should be True, as this is a test.
grind_method(grind_target, num_items(grind_target) + WANTED_AMOUNT, True, True)

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
#pumpkin_smart(10) # This should really be called from grind_method() instead..

# Power:
#old_method_sunflower(num_items(Items.Power) + WANTED_AMOUNT)
#get_power(num_items(Items.Power) + WANTED_AMOUNT)

# Gold:
#do_simple_maze_run(num_items(Items.Gold) + WANTED_AMOUNT)

# Cacti:
#cactus_bubble(num_items(Items.Cactus) + WANTED_AMOUNT)
#cactus_shaker(num_items(Items.Cactus) + WANTED_AMOUNT)

# Bones:
#ultra_dumb_dyno(num_items(Items.Bones) + WANTED_AMOUNT)
#dyno_slightly_smarter(num_items(Items.Bones) + WANTED_AMOUNT)
