import random


# ===================================== Generators ================================================
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
DURATION_COEFFICIENT = 1  # Used to crawl more safely.
MINUTE = 60

CLICK_SLEEP = random_double_generator(
    5 * DURATION_COEFFICIENT, 7.5 * DURATION_COEFFICIENT
)
ENTER_DATA_SLEEP = random_double_generator(
    7.5 * DURATION_COEFFICIENT, 15 * DURATION_COEFFICIENT
)
WAIT_FOR_RESPONSE_SLEEP = random_double_generator(
    15 * DURATION_COEFFICIENT, 20 * DURATION_COEFFICIENT
)
CRAWL_FINISHED_SLEEP = random_double_generator(
    5 * MINUTE * DURATION_COEFFICIENT, 10 * MINUTE * DURATION_COEFFICIENT
)

SECONDS_UNTIL_TIMEOUT = 10

# ===================================== Scrolling =================================================
# TODO Ponder: how much can we scroll etc
SCROLL_LENGTH_INSIDE_POPUP = random_int_generator(5, 8)
SCROLL_LENGTH_ON_WEBSITE = random_int_generator(2000, 4000)
SCROLL_UPWARDS = random_bool_generator(0.2)

# ===================================== Instagram Login ============================= ==============
# LOG_IN_USERNAME = "stefandovakin"
# LOG_IN_PASSWORD = "dragonborn1234"

# Temp Mail.org
LOG_IN_USERNAMES = ["xeyos10054@5sword.com"]
LOG_IN_USERNAME = LOG_IN_USERNAMES[0]
LOG_IN_PASSWORD = "crawler_69"

# ===================================== Default values ============================================
INSTAGRAM_START_PAGE = "https://www.instagram.com/"
MARRYICETEA_INSTAGRAM_USERNAME = "marryicetea"

MAXIMAL_POSTS_OF_CONSUMERS = 25
POSITION_OF_LIKES_BOX = 0
POSITION_OF_FOLLOWERS_BOX = 1
POSITION_OF_FOLLOWING_BOX = 2

# ===================================== Paths =====================================================
COMPANY_PATH = "items/companies/"
CONSUMER_PATH = "items/consumers/"

# ===================================== Xpath constants ===========================================
XPATH_TO_SEARCH_FOR_USERNAME_BOX = "//input[@placeholder='Search']"

XPATH_TO_PROFILE_NUMBER_OF_POSTS = '//*[@class="g47SY "]/text()'
XPATH_TO_PROFILE_FOLLOWERS = '//*[@class="g47SY "]/text()'
XPATH_TO_PROFILE_FOLLOWING = '//*[@class="g47SY "]/text()'
XPATH_TO_PROFILE_DESCRIPTION = '//*[@class="-vDIg"]/*/text()'
XPATH_TO_PROFILE_HASHTAGS = '//*[@class="-vDIg"]/*/*/text()'
XPATH_TO_PROFILE_OTHER_TAGS = '//*[@class="-vDIg"]/*/*/text()'
XPATH_TO_PROFILE_LIFESTYLE_STORIES = '//*[@class="eXle2"]/text()'
XPATH_TO_PROFILE_IS_PRIVATE = '//*[contains(text(), "This Account is Private")]'
XPATH_TO_POST_FOLLOWING_BOX = '//*[@class="g47SY "]'
XPATH_TO_POST_USERS_WHO_WE_FOLLOW = '//*[@class="FPmhX notranslate  _0imsa "]/text()'
XPATH_TO_POST_ELEMENT_INSIDE_FOLLOWING_POPUP = '//*[@class="Jv7Aj mArmR MqpiF  "]/*'
XPATH_TO_POST_FOLLOWERS_BOX = '//*[@class="g47SY "]'
XPATH_TO_POST_USERS_WHO_FOLLOW_US = '//*[@class="FPmhX notranslate  _0imsa "]/text()'
XPATH_TO_POST_ELEMENT_INSIDE_FOLLOWERS_POPUP = '//*[@class="Jv7Aj mArmR MqpiF  "]/*'
XPATH_TO_PROFILE_POPUP_EXIT_BUTTON = '//*[@class="QBdPU "]'

XPATH_TO_POST_LIKES = '//*[@class="zV_Nj"]/span/text()'
XPATH_TO_POST_HASHTAGS = '//a[@class=" xil3i"]'
XPATH_TO_POST_DESCRIPTION = '//*[@class="C4VMK"]/span/text()'
XPATH_TO_POST_USERS_WHO_LIKED_IT = '//*[@class="FPmhX notranslate MBL3Z"]/text()'
XPATH_TO_POST_DATE = '//*[@class="_1o9PC Nzb55"]/@datetime'
XPATH_TO_POST_LIKES_BOX = '//a[@class="zV_Nj"]'
XPATH_TO_POST_ELEMENT_INSIDE_LIKES_POPUP = '//*[@class="FPmhX notranslate MBL3Z"]'

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
IS_PRIVATE = "is_private"
FOLLOWING_NAMES = "following_names"
FOLLOWERS_NAMES = "followers_names"

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
    IS_PRIVATE,
    FOLLOWING_NAMES,
    FOLLOWERS_NAMES,
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
