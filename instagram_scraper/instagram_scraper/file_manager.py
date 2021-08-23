import datetime
import os
from time import sleep

import wget
from urllib.error import HTTPError

from instagram_scraper.constants import *
from instagram_scraper.csv_handler import CSVHandler


class FileManager:
    def __init__(
        self,
        is_a_company,
        username,
    ):
        self.is_a_company = is_a_company
        working_directory = os.getcwd()
        self.csv_handler = CSVHandler()

        if is_a_company:
            self.csv_path = os.path.join(working_directory, COMPANY_PATH, username)
            self.image_path = os.path.join(
                working_directory, COMPANY_PATH, username, "images"
            )
        else:
            self.csv_path = os.path.join(working_directory, CONSUMER_PATH, username)
            self.image_path = os.path.join(
                working_directory, CONSUMER_PATH, username, "images"
            )

        current_date = datetime.datetime.now()
        csv_file_name = f"profile_data - {current_date.day}.{current_date.month}.{current_date.year}.csv"
        self.csv_profile_path = os.path.join(self.csv_path, csv_file_name)

    # ===================================== Safe Items ============================================
    def safe_profile_data(self, profile_item):
        has_profile_data = os.path.isfile(self.csv_profile_path)

        # TODO do i even need this check anymore? or could we just check the profile items for none?
        if not has_profile_data or self.is_a_company:
            self.csv_handler.write_profile_data(self.csv_profile_path, profile_item)

    def safe_post_data(self, post_items):
        csv_post_path = os.path.join(self.csv_path, "posts_data.csv")
        has_file_entries = os.path.isfile(csv_post_path)
        self.csv_handler.write_post_data(csv_post_path, has_file_entries, post_items)

    # ===================================== Download Images =======================================
    def safe_image(self, post_items):
        urls_of_images = post_items.get_collected_values(URL_OF_POST)
        id_of_posts = post_items.get_collected_values(ID_OF_POST)
        try:
            self._download_images(id_of_posts, urls_of_images)
        except HTTPError as exception:
            print("Download was not possible - the exception:")
            print(exception)

    def _download_images(self, id_of_posts, urls_of_images):
        for id_of_post, url_of_image in zip(id_of_posts, urls_of_images):
            save_to_location = os.path.join(self.image_path, id_of_post + ".jpg")
            wget.download(url_of_image, save_to_location)
            sleep(WAIT_FOR_RESPONSE_SLEEP)

    # ===================================== Utility ===============================================
    @staticmethod
    def _create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

    # ===================================== Utility Public ===============================================
    def create_directories(self):
        self._create_directory(self.csv_path)
        self._create_directory(self.image_path)

    def has_profile_data(self):
        return os.path.isfile(self.csv_profile_path)

    def already_crawled_urls(self):
        csv_post_path = os.path.join(self.csv_path, "posts_data.csv")
        has_file_entries = os.path.isfile(csv_post_path)

        if has_file_entries:
            return self.csv_handler.already_crawled_urls(csv_post_path)
        return set()

    def delete_row_from_user_to_crawl_csv(self, path_to_users_to_crawl_csv):
        self.csv_handler.delete_row_from_user_to_crawl_csv(path_to_users_to_crawl_csv)

    def users_from_csv(self, users_to_load_from_csv):
        working_directory = os.getcwd()
        path_to_users_to_crawl_csv = os.path.join(
            working_directory, "users_to_crawl.csv"
        )

        return self.csv_handler.users_from_csv(
            path_to_users_to_crawl_csv, users_to_load_from_csv
        )

    @staticmethod
    def create_information_file(username, usernames):

        with open("information.txt", "w") as file:
            file.write(
                f"We are logged in as: {LOG_IN_USERNAME}.\n"
                f"Currently we are scraping {username}.\n"
                f"He is on position {usernames.index(username) + 1} / {len(usernames)}."
            )
