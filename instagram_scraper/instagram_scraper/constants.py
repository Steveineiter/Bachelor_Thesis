import random


# TODO Ask: can we put the random stuffs in a generator? because atm they are static right?
#    Like this:
def random_double_generator(lower_limit, upper_limit):
    while True:
        yield round(random.uniform(lower_limit, upper_limit), 2)


def random_int_generator(lower_limit, upper_limit):
    while True:
        yield random.randint(lower_limit, upper_limit)


CLICK_SLEEP = random_double_generator(
    0.5, 1.5
)  # TODO Ask: can we code it so that CLICK_SLEEP == next(CLICK_SLEEP)?
ENTER_DATA_SLEEP = random_double_generator(1.5, 3.5)
WAIT_FOR_RESPONSE_SLEEP = random_double_generator(5, 7.5)

SECONDS_UNTIL_TIMEOUT = 10

SCROLL_LENGTH_INSIDE_POPUP = random_int_generator(8, 10)

INSTAGRAM_START_PAGE = "https://www.instagram.com/"
MARRYICETEA_INSTAGRAM_USERNAME = "marryicetea"
CSV_HEADER_ITEMS = [
    "id_of_post",
    "url_of_post",
    "likes_of_post",
    "hashtags_of_post",
    "description_of_post",
    "post_was_liked_by",
]
