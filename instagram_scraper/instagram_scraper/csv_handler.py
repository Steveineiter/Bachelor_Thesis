import csv
from instagram_scraper.constants import *


class CSVHandler:
    def __init__(self):
        pass

    # ===================================== Write Profile =========================================
    def write_profile_data(self, csv_profile_path, profile_item):
        profile_csv_file = open(csv_profile_path, "w")
        profile_writer = csv.writer(profile_csv_file)

        self.write_csv_header(profile_writer, PROFILE_CSV_HEADER_ITEMS)
        self.write_csv_profile_item(profile_writer, profile_item)

        profile_csv_file.close()

    @staticmethod
    def write_csv_profile_item(profile_writer, item_loader):
        profile_writer.writerow(
            [
                " ".join(item_loader.get_collected_values(NAME_OF_PROFILE)),
                " ".join(item_loader.get_collected_values(NUMBER_OF_POSTS)),
                " ".join(item_loader.get_collected_values(FOLLOWERS)),
                " ".join(item_loader.get_collected_values(FOLLOWING)),
                " ".join(item_loader.get_collected_values(DESCRIPTION_OF_PROFILE)),
                " ".join(item_loader.get_collected_values(HASHTAGS_OF_DESCRIPTION)),
                " ".join(item_loader.get_collected_values(OTHER_TAGS_OF_DESCRIPTION)),
                " ".join(item_loader.get_collected_values(LIFESTYLE_STORIES)),
                " ".join(item_loader.get_collected_values(IS_PRIVATE)),
                " ".join(item_loader.get_collected_values(FOLLOWING_NAMES)),
            ]
        )

    # ===================================== Write Posts ===========================================

    def write_post_data(self, csv_post_path, has_file_entries, post_items):
        posts_csv_file = open(csv_post_path, "a")
        posts_writer = csv.writer(posts_csv_file)

        if not has_file_entries:
            self.write_csv_header(posts_writer, POSTS_CSV_HEADER_ITEMS)
        self.write_csv_post_items(posts_writer, post_items)

        posts_csv_file.close()

    @staticmethod
    def write_csv_post_items(posts_writer, item_loader):
        # TODO Ask: Is there a better way for the next 2 lines?
        item_loader_likes_of_post = item_loader.get_collected_values(LIKES_OF_POST)
        item_loader_post_was_liked_by = item_loader.get_collected_values(
            POST_WAS_LIKED_BY
        )
        posts_writer.writerow(
            [
                " ".join(item_loader.get_collected_values(ID_OF_POST)),
                " ".join(item_loader.get_collected_values(URL_OF_POST)),
                " ".join(item_loader_likes_of_post)
                if len(item_loader_likes_of_post) > 0
                else None,
                " ".join(item_loader.get_collected_values(HASHTAGS_OF_POST)),
                " ".join(item_loader.get_collected_values(DESCRIPTION_OF_POST)),
                " ".join(item_loader_post_was_liked_by)
                if len(item_loader_likes_of_post) > 0
                else None,
                " ".join(item_loader.get_collected_values(DATE_OF_POST)),
            ]
        )

    # ===================================== Utility ===============================================
    @staticmethod
    def write_csv_header(writer, header_items):
        writer.writerow(header_items)

    @staticmethod
    def already_crawled_urls(csv_post_path):
        already_crawled_urls = set()
        with open(
            csv_post_path,
        ) as posts_csv_file:
            dict_reader = csv.DictReader(posts_csv_file)
            for row in dict_reader:
                already_crawled_urls.add(row["url_of_post"])
        return already_crawled_urls
