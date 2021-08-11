import random
# TODO can we put the random stuffs in a generator? because atm they are static right?

CLICK_SLEEP = round(random.uniform(0.5, 1.5), 2)
ENTER_DATA_SLEEP = round(random.uniform(1.5, 3.5), 2)
WAIT_FOR_RESPONSE_SLEEP = round(random.uniform(5, 7.5), 2)

SECONDS_FOR_TIMEOUT = 10

SCROLL_LENGTH = random.randint(8, 10)
