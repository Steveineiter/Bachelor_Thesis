import random


# TODO Ask: can we put the random stuffs in a generator? because atm they are static right?
#    Like this:
def random_double_generator(lower_limit, upper_limit):
    while True:
        yield round(random.uniform(lower_limit, upper_limit), 2)


def random_int_generator(lower_limit, upper_limit):
    while True:
        yield random.randint(lower_limit, upper_limit)


def random_bool_generator(chance_for_true_result):
    while True:
        yield random.random() < chance_for_true_result


DURATION_COEFFICIENT = 2  # Used to crawl more safely.
CLICK_SLEEP = random_double_generator(
    0.5 * DURATION_COEFFICIENT, 1.5 * DURATION_COEFFICIENT
)  # TODO Ask: can we code it so that CLICK_SLEEP == next(CLICK_SLEEP)?
ENTER_DATA_SLEEP = random_double_generator(
    1.5 * DURATION_COEFFICIENT, 3.5 * DURATION_COEFFICIENT
)
WAIT_FOR_RESPONSE_SLEEP = random_double_generator(
    5 * DURATION_COEFFICIENT, 7.5 * DURATION_COEFFICIENT
)

SECONDS_UNTIL_TIMEOUT = 10

SCROLL_LENGTH_INSIDE_POPUP = random_int_generator(8, 10)
SCROLL_LENGTH_ON_WEBSITE = random_int_generator(
    2000, 6000
)  # TODO Ponder: how much can we scroll etc
SCROLL_UPWARDS = random_bool_generator(0.2)

INSTAGRAM_START_PAGE = "https://www.instagram.com/"
MARRYICETEA_INSTAGRAM_USERNAME = "marryicetea"
LOG_IN_PASSWORD = "dragonborn1234"
LOG_IN_USERNAME = "stefandovakin"

POSTS_CSV_HEADER_ITEMS = [
    "id_of_post",
    "url_of_post",
    "likes_of_post",
    "hashtags_of_post",
    "description_of_post",
    "post_was_liked_by",
    "date_of_post",
]

PROFILE_CSV_HEADER_ITEMS = [
    "name_of_profile",
    "number_of_posts",
    "followers",
    "following",
    "description_of_profile",
    "hashtags_of_description",
    "other_tags_of_description",
    "lifestyle_stories",
]

COMPANY_PATH = "items/companies/"
CONSUMER_PATH = "items/consumers/"


# TODO: Extract all instagram classes -> because they are ugly to read and it would be better to modify.
INSTAGRAM_POSTS_CLASS_TAG = "g47SY "
