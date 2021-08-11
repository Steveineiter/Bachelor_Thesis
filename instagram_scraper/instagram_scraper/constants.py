import random


# TODO Ask: can we put the random stuffs in a generator? because atm they are static right?
#    Like this:
def random_double_generator(lower_limit, upper_limit):
    while True:
        yield round(random.uniform(lower_limit, upper_limit), 2)


def random_int_generator(lower_limit, upper_limit):
    while True:
        yield random.randint(lower_limit, upper_limit)


CLICK_SLEEP = random_double_generator(0.5, 1.5)  # TODO Ask: can we code it so that CLICK_SLEEP == next(CLICK_SLEEP)?
ENTER_DATA_SLEEP = random_double_generator(1.5, 3.5)
WAIT_FOR_RESPONSE_SLEEP = random_double_generator(5, 7.5)

SECONDS_UNTIL_TIMEOUT = 10

SCROLL_LENGTH = random_int_generator(8, 10)

MARRYICETEA_INSTAGRAM_USERNAME = "marryicetea"