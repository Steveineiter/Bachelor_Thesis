import random

# Generators:
def random_int_generator(lower_limit, upper_limit):
    while True:
        yield random.randint(lower_limit, upper_limit)


def random_double_generator(lower_limit, upper_limit):
    while True:
        yield round(random.uniform(lower_limit, upper_limit), 2)

# Constants:
TWITTER_START_PAGE = "https://twitter.com/login"
TWITTER_LIPTON_PAGE = "https://www.twitter.com/lipton"
MAXIMAL_FOLLOWERS = 1000

PAGE_HEIGHT_SCRIPT = "return document.body.scrollHeight"
TOTAL_SCROLLED_HEIGHT_SCRIPT = "return window.pageYOffset + window.innerHeight"
SCROLL_LENGTH_ON_WEBSITE = random_int_generator(2000, 4000)
ENTER_DATA_SLEEP = random_double_generator(
    1, 3
)
WAIT_FOR_RESPONSE_SLEEP = random_double_generator(
    9, 12
)