import csv


class checklistCreator:
    def create_checklist(self):
        # TODO Ask: what is in this case smarter? static methods like this or just as pycharm
        #  would handle it (extract it from class)?
        id_of_post_to_post_was_liked_by = (
            checklist_creator.id_of_post_to_post_was_liked_by()
        )
        user_to_liked_posts_count_and_id = self.user_to_liked_posts_count_and_id(
            id_of_post_to_post_was_liked_by
        )
        self.safe_data_in_csv(user_to_liked_posts_count_and_id)

    @staticmethod
    def id_of_post_to_post_was_liked_by():
        # open CSV
        id_of_post_to_post_was_liked_by = {}

        with open("marry_items.csv", newline="") as marry_csv_file:
            dict_reader = csv.DictReader(marry_csv_file)
            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                print(row["id_of_post"], row["post_was_liked_by"])
                id_of_post_to_post_was_liked_by[row["id_of_post"]] = row[
                    "post_was_liked_by"
                ]

        return id_of_post_to_post_was_liked_by

    @staticmethod
    def user_to_liked_posts_count_and_id(id_of_post_to_post_was_liked_by):
        # Put names in dict and count it (Person: (counter, id_of_post))
        user_to_liked_posts_count_and_id = {}

        for id_of_post, post_was_liked_by in id_of_post_to_post_was_liked_by.items():
            users = [str(user) for user in post_was_liked_by.split(" ")]
            for user in users:
                if user in user_to_liked_posts_count_and_id:
                    user_to_liked_posts_count_and_id[user] = (
                        user_to_liked_posts_count_and_id[user][0] + 1,
                        user_to_liked_posts_count_and_id[user][1] + " " + id_of_post,
                    )
                else:
                    user_to_liked_posts_count_and_id[user] = (1, id_of_post)

        return user_to_liked_posts_count_and_id

    @staticmethod
    def safe_data_in_csv(user_to_liked_posts_count_and_id):
        # Safe dict in CSV with columns Person, counter
        with open("marry_checklist.csv", "w", newline="") as marry_checklist_csv_file:
            fieldnames = ["user", "liked_posts_count", "id_of_post"]
            dict_writer = csv.DictWriter(
                marry_checklist_csv_file, fieldnames=fieldnames
            )

            dict_writer.writeheader()
            for (
                user,
                liked_posts_count_and_id,
            ) in user_to_liked_posts_count_and_id.items():
                liked_posts_count, id_of_post = liked_posts_count_and_id
                dict_writer.writerow(
                    {
                        "user": user,
                        "liked_posts_count": liked_posts_count,
                        "id_of_post": id_of_post,
                    }
                )


if __name__ == "__main__":
    checklist_creator = checklistCreator()
    checklist_creator.create_checklist()
