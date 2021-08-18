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
            self.csv_path = os.path.join(
                working_directory, os.pardir, COMPANY_PATH, username
            )
            self.image_path = os.path.join(
                working_directory, os.pardir, COMPANY_PATH, username, "images"
            )
        else:
            self.csv_path = os.path.join(
                working_directory, os.pardir, CONSUMER_PATH, username
            )
            self.image_path = os.path.join(
                working_directory, os.pardir, CONSUMER_PATH, username, "images"
            )

        self.csv_profile_path = os.path.join(self.csv_path, "profile_data.csv")
        # self.create_directory(self.csv_path)
        # self.create_directory(self.image_path)

        # csv_profile_path = os.path.join(self.csv_path, "profile_data.csv")
        # self.has_profile_data = os.path.isfile(csv_profile_path)
        # if not self.has_profile_data or is_a_company:
        #     self.profile_csv_file = open(
        #         os.path.join(self.csv_path, "profile_data.csv"), "w"
        #     )
        #     self.profile_writer = csv.writer(self.profile_csv_file)
        #     self.write_csv_header(self.profile_writer, PROFILE_CSV_HEADER_ITEMS)

        # if is_a_deep_crawl:
        # csv_post_path = os.path.join(self.csv_path, "posts_data.csv")
        # has_file_entries = os.path.isfile(csv_post_path)
        # if has_file_entries:
        #     with open(
        #             csv_post_path,
        #     ) as posts_csv_file:
        #         dict_reader = csv.DictReader(posts_csv_file)
        #         for row in dict_reader:
        #             self.already_crawled_urls.add(row["url_of_post"])

        # self.posts_csv_file = open(csv_post_path, "a")
        # self.posts_writer = csv.writer(self.posts_csv_file)
        # if not has_file_entries:
        #     self.write_csv_header(self.posts_writer, POSTS_CSV_HEADER_ITEMS)

    def save_crawled_data(self, profile_item, post_items):
        self._create_directories()

        self._safe_profile_data(profile_item)
        self._safe_post_data(post_items)
        try:
            self._safe_images(post_items)
        except HTTPError:
            pass

        # TODO Implement:
        # if path_for_crawl_list_is_given:
        #     self.delete_crawl_list_entry

    # ===================================== Safe Items ============================================
    def _safe_profile_data(self, profile_item):
        csv_profile_path = os.path.join(self.csv_path, "profile_data.csv")
        has_profile_data = os.path.isfile(csv_profile_path)

        # TODO do i even need this check anymore? or could we just check the profile items for none?
        if (
            not has_profile_data or self.is_a_company
        ):
            self.csv_handler.write_profile_data(csv_profile_path, profile_item)

    def _safe_post_data(self, post_items):
        csv_post_path = os.path.join(self.csv_path, "posts_data.csv")
        has_file_entries = os.path.isfile(csv_post_path)
        self.csv_handler.write_post_data(
            csv_post_path, has_file_entries, post_items
        )

    # ===================================== Download Images =======================================
    def _safe_images(self, post_items):
        urls_of_images = post_items.get_collected_values(URL_OF_POST)
        id_of_posts = post_items.get_collected_values(ID_OF_POST)

        self._download_images(id_of_posts, urls_of_images)

    def _download_images(self, id_of_posts, urls_of_images):
        for id_of_post, url_of_image in zip(id_of_posts, urls_of_images):
            save_to_location = os.path.join(self.image_path, id_of_post + ".jpg")
            wget.download(url_of_image, save_to_location)
            sleep(WAIT_FOR_RESPONSE_SLEEP)

    # ===================================== Utility ===============================================
    def _create_directories(self):
        self._create_directory(self.csv_path)
        self._create_directory(self.image_path)

    @ staticmethod
    def _create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)

    # ===================================== Utility Public ===============================================
    def has_profile_data(self):
        return os.path.isfile(self.csv_profile_path)

    def already_crawled_urls(self):
        csv_post_path = os.path.join(self.csv_path, "posts_data.csv")
        has_file_entries = os.path.isfile(csv_post_path)

        if has_file_entries:
            return self.csv_handler.already_crawled_urls(csv_post_path)
        return set()
