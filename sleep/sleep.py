import random
import time
def random_sleep(min=1,max=5.0):
	seed=random.uniform(min,max)
	time.sleep(seed)