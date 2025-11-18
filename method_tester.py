import farm_bones
import farm_cactus
import farm_gold
import farm_power
import farm_pumpkins
import farm_trifecta
from resource_management import grind_method

START_TIME = get_time()
clear()
# set_farm_size(7)
# set_execution_speed(10)

# To use or test any of the grinding functions, remove the "#"
# Some of them may assume you have the requirements to run them (seeds or fert)


WANTED_AMOUNT = 100 * 1000 * 1000  # This is how much MORE than you currently have you want
WANTED_RUNS = 100  # For run based methods
default_poly = Items.Carrot
grind_target = Items.Pumpkin

# The third parameter in grind_method is whether or not to get power first.
# The fourth parameter in grind_method should be True, as this is a test.
grind_method(grind_target, num_items(grind_target) + WANTED_AMOUNT, True, True)


# Hay:
farm_trifecta.hay_full_field(num_items(Items.Hay) + WANTED_AMOUNT)
farm_trifecta.hay_vertical(num_items(Items.Hay) + WANTED_AMOUNT)


# Wood:
farm_trifecta.one_by_three_bush_hay_wait(num_items(Items.Wood) + WANTED_AMOUNT)
farm_trifecta.three_by_three_with_hay(num_items(Items.Wood) + WANTED_AMOUNT)
farm_trifecta.tree_and_bush(num_items(Items.Wood) + WANTED_AMOUNT)


# Carrots:
farm_trifecta.carrot_three_by_three(num_items(Items.Carrot) + WANTED_AMOUNT)
farm_trifecta.carrots_trusting(num_items(Items.Carrot) + WANTED_AMOUNT)

# Polyculture (Choose what to prioritize):
farm_trifecta.poly_farm(default_poly, num_items(default_poly) + WANTED_AMOUNT)

# Pumpkins:
farm_pumpkins.pumpkin_smart(10)
farm_pumpkins.pumpkin_multi(1000)

# Power:
farm_power.get_power(num_items(Items.Power) + WANTED_AMOUNT)

# Gold:
farm_gold.do_simple_maze_runs(WANTED_RUNS)
farm_gold.maze_branch_based(WANTED_RUNS)

# Cacti:
farm_cactus.cactus_bubble(num_items(Items.Cactus) + WANTED_AMOUNT)
farm_cactus.cactus_shaker(num_items(Items.Cactus) + WANTED_AMOUNT)

# Bones:
farm_bones.prepare_dinosaurs()
farm_bones.snake_basic(num_items(Items.Bone) + WANTED_AMOUNT)
farm_bones.snake_fill_farm(WANTED_RUNS)