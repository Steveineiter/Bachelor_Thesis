import random


# ===================================== Generators ================================================
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


# ===================================== Random sleeping, to make it more organic ==================
# TODO Ask: can we code it so that CLICK_SLEEP = next(CLICK_SLEEP)?
DURATION_COEFFICIENT = 2  # Used to crawl more safely.

CLICK_SLEEP = random_double_generator(
    0.5 * DURATION_COEFFICIENT, 1.5 * DURATION_COEFFICIENT
)
ENTER_DATA_SLEEP = random_double_generator(
    1.5 * DURATION_COEFFICIENT, 3.5 * DURATION_COEFFICIENT
)
WAIT_FOR_RESPONSE_SLEEP = random_double_generator(
    5 * DURATION_COEFFICIENT, 7.5 * DURATION_COEFFICIENT
)
CRAWL_FINISHED_SLEEP = random_double_generator(
    2.5 * 60 * DURATION_COEFFICIENT, 7.5 * 60 * DURATION_COEFFICIENT
)

SECONDS_UNTIL_TIMEOUT = 10

# ===================================== Scrolling =================================================
# TODO Ponder: how much can we scroll etc
SCROLL_LENGTH_INSIDE_POPUP = random_int_generator(8, 10)
SCROLL_LENGTH_ON_WEBSITE = random_int_generator(2000, 6000)
SCROLL_UPWARDS = random_bool_generator(0.2)

# ===================================== Instagram Login ===========================================
LOG_IN_PASSWORD = "dragonborn1234"
LOG_IN_USERNAME = "stefandovakin"

# ===================================== Default values ============================================
INSTAGRAM_START_PAGE = "https://www.instagram.com/"
MARRYICETEA_INSTAGRAM_USERNAME = "marryicetea"

# ===================================== Paths =====================================================
COMPANY_PATH = "items/companies/"
CONSUMER_PATH = "items/consumers/"


# TODO: Extract all instagram classes -> because they are ugly to read and it would be better to modify.
# ===================================== Xpath constants ===========================================
XPATH_TO_SEARCH_FOR_USERNAME_BOX = "//input[@placeholder='Search']"

XPATH_TO_PROFILE_NUMBER_OF_POSTS = '//*[@class="g47SY "]/text()'
XPATH_TO_PROFILE_FOLLOWERS = '//*[@class="g47SY "]/text()'
XPATH_TO_PROFILE_FOLLOWING = '//*[@class="g47SY "]/text()'
XPATH_TO_PROFILE_DESCRIPTION = '//*[@class="-vDIg"]/*/text()'
XPATH_TO_PROFILE_HASHTAGS = '//*[@class="-vDIg"]/*/*/text()'
XPATH_TO_PROFILE_OTHER_TAGS = '//*[@class="-vDIg"]/*/*/text()'
XPATH_TO_PROFILE_LIFESTYLE_STORIES = '//*[@class="eXle2"]/text()'

XPATH_TO_POST_LIKES = '//*[@class="zV_Nj"]/span/text()'
XPATH_TO_POST_HASHTAGS = '//a[@class=" xil3i"]'
XPATH_TO_POST_DESCRIPTION = '//*[@class="C4VMK"]/span/text()'
XPATH_TO_POST_USERS_WHO_LIKED_IT = '//*[@class="FPmhX notranslate MBL3Z"]/text()'
XPATH_TO_POST_DATE = '//*[@class="_1o9PC Nzb55"]/@datetime'
XPATH_TO_POST_LIKES_BOX = '//a[@class="zV_Nj"]'
XPATH_TO_POST_ELEMENT_INSIDE_POPUP = '//*[@class="FPmhX notranslate MBL3Z"]'

# ===================================== Scripts ===================================================
PAGE_HEIGHT_SCRIPT = "return document.body.scrollHeight"
TOTAL_SCROLLED_HEIGHT_SCRIPT = "return window.pageYOffset + window.innerHeight"

# ===================================== Loader Items ==============================================
# Note: If you change something here, also change in items class.

# ProfileDataItem
NAME_OF_PROFILE = "name_of_profile"
NUMBER_OF_POSTS = "number_of_posts"
FOLLOWERS = "followers"
FOLLOWING = "following"
DESCRIPTION_OF_PROFILE = "description_of_profile"
HASHTAGS_OF_DESCRIPTION = "hashtags_of_description"
OTHER_TAGS_OF_DESCRIPTION = "other_tags_of_description"
LIFESTYLE_STORIES = "lifestyle_stories"

# PostDataItem
ID_OF_POST = "id_of_post"
URL_OF_POST = "url_of_post"
LIKES_OF_POST = "likes_of_post"
HASHTAGS_OF_POST = "hashtags_of_post"
DESCRIPTION_OF_POST = "description_of_post"
POST_WAS_LIKED_BY = "post_was_liked_by"
DATE_OF_POST = "date_of_post"

# ===================================== CSV Items =================================================
PROFILE_CSV_HEADER_ITEMS = [
    NAME_OF_PROFILE,
    NUMBER_OF_POSTS,
    FOLLOWERS,
    FOLLOWING,
    DESCRIPTION_OF_PROFILE,
    HASHTAGS_OF_DESCRIPTION,
    OTHER_TAGS_OF_DESCRIPTION,
    LIFESTYLE_STORIES,
]

POSTS_CSV_HEADER_ITEMS = [
    ID_OF_POST,
    URL_OF_POST,
    LIKES_OF_POST,
    HASHTAGS_OF_POST,
    DESCRIPTION_OF_POST,
    POST_WAS_LIKED_BY,
    DATE_OF_POST,
]
