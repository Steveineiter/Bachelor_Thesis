import csv
import random
from nltk.corpus import names
import nltk
nltk.download('names')


class PostsCSVDataCreator:
    def create_posts_csv_data(self):
        id_of_post_to_data = posts_csv_data_creator.id_of_post_to_data()
        csv_data_to_safe = self.csv_data_to_safe(
            id_of_post_to_data
        )
        self.safe_data_in_csv(csv_data_to_safe)

    @staticmethod
    def id_of_post_to_data():
        # open CSV
        id_of_post_to_data = {}

        # TODO add DATE after new crawling
        with open("marry_items.csv", newline="") as marry_csv_file:
            dict_reader = csv.DictReader(marry_csv_file)
            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                id_of_post_to_data[row["id_of_post"]] = (
                    row["url_of_post"],
                    row["description_of_post"],
                    row["likes_of_post"],
                    row["post_was_liked_by"],
                )

        return id_of_post_to_data

    def csv_data_to_safe(self, id_of_post_to_data):
        # Put names in dict and count it (Person: (counter, id_of_post))
        csv_data_to_safe = {}

        # TODO add link to user after more crawling
        for id_of_post, data in id_of_post_to_data.items():
            url_of_post, description_of_post, likes_of_post, post_was_liked_by = data
            # Innerhalb vom table haben wir noch einen table
            information_of_users = self.information_of_users(post_was_liked_by)
            gender_distribution = self.gender_distribution(information_of_users)

            date_of_post = ""
            csv_data_to_safe[id_of_post] = (url_of_post, description_of_post, likes_of_post, gender_distribution, information_of_users, date_of_post)

        return csv_data_to_safe

    def information_of_users(self, post_was_liked_by):
        information_of_users = []
        user_names = [str(user) for user in post_was_liked_by.split(" ")]

        for user_name in user_names:
            gender_of_user = self.gender_of_user(user_name)
            information_of_users.append((user_name, gender_of_user))

        return information_of_users

    @staticmethod
    def gender_of_user(user_name):
        male_names = names.words('male.txt')
        female_names = names.words('female.txt')
        male_counter = 0
        female_counter = 0

        for male_name in male_names:
            if male_name.upper() in user_name.upper():
                male_counter += 1

        for female_name in female_names:
            if female_name.upper() in user_name.upper():
                female_counter += 1

        if male_counter > female_counter:
            return "M"
        if male_counter < female_counter:
            return "W"
        return "Other"  # If we are not sure. Eg 2 male names, 2 female names -> Other.

    @staticmethod
    def gender_distribution(information_of_users):
        male_counter = 0
        female_counter = 0

        for _, gender in information_of_users:
            if gender == "M":
                male_counter += 1
            if gender == "W":
                female_counter += 1
        try:
            return f"{round(male_counter / (male_counter + female_counter) * 100)}% / {round(female_counter / (male_counter + female_counter) * 100)}%"
        except ZeroDivisionError:
            # In case there are no likes/users, eg at videos.
            return "N/A"

    @staticmethod
    def safe_data_in_csv(csv_data_to_safe):
        # Safe dict in CSV with columns Person, counter
        with open("data_for_html.csv", "w", newline="") as marry_data_for_html_csv_file:
            fieldnames = ["url_of_post", "description_of_post", "likes_of_post", "male/female", "information_of_users", "Date - TODO with new crawled data"]
            dict_writer = csv.DictWriter(
                marry_data_for_html_csv_file, fieldnames=fieldnames
            )

            dict_writer.writeheader()
            for (
                _,
                data,
            ) in csv_data_to_safe.items():
                url_of_post, description_of_post, likes_of_post, gender_distribution, information_of_users, date_of_post = data
                dict_writer.writerow(
                    {
                        "url_of_post": url_of_post,
                        "description_of_post": description_of_post,
                        "likes_of_post": likes_of_post,
                        "male/female": gender_distribution,
                        "information_of_users": information_of_users,
                        "Date - TODO with new crawled data": date_of_post
                    }
                )


if __name__ == "__main__":
    posts_csv_data_creator = PostsCSVDataCreator()
    posts_csv_data_creator.create_posts_csv_data()
