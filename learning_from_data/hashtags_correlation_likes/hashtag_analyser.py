import csv


# TODO crossvalidation und visualisierung waere noch cool
class hashtagAnalyser:
    def create_hashtag_likes_csv(self):
        hashtag_to_occurences_and_average_likes = self.hashtag_to_occurences_and_average_likes()
        self.safe_data_in_csv(
            hashtag_to_occurences_and_average_likes
        )

    @staticmethod
    def hashtag_to_occurences_and_average_likes():
        # open CSV
        hashtag_to_occurences_and_average_likes = {}

        # TODO add DATE after new crawling
        with open("marry_items.csv", newline="") as marry_csv_file:
            dict_reader = csv.DictReader(marry_csv_file)
            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                hashtags = row["hashtags_of_post"].split()
                likes = row["likes_of_post"]

                for hashtag in hashtags:
                    hashtag = "".join((filter(str.isalnum, hashtag)))
                    if "#" + hashtag in hashtag_to_occurences_and_average_likes.keys():
                        hashtag_to_occurences_and_average_likes["#" + hashtag][0] += 1
                        if not likes:
                            likes = 0
                        hashtag_to_occurences_and_average_likes["#" + hashtag][1] = int(hashtag_to_occurences_and_average_likes["#" + hashtag][1]) + int(likes)
                    else:
                        if not likes:
                            likes = 0
                        hashtag_to_occurences_and_average_likes["#" + hashtag] = [1, likes]
        print("Hashtags   |    number of posts with this hashtag    | likes  ")
        for key, data in hashtag_to_occurences_and_average_likes.items():
            used_in_posts, likes = data
            print(key, " " * 5, used_in_posts, " " * 5, likes, " " * 5)
        return hashtag_to_occurences_and_average_likes

    @staticmethod
    def safe_data_in_csv(hashtag_to_occurences_and_average_likes):
        with open("hashtags_likes_correlation.csv", "w", newline="") as hashtags_likes_correlation_csv_file:
            fieldnames = ["hashtag", "average_likes", "number_of_posts_with_this_hashtag"]
            dict_writer = csv.DictWriter(
                hashtags_likes_correlation_csv_file, fieldnames=fieldnames
            )

            dict_writer.writeheader()
            for (
                    hashtag,
                    data,
            ) in hashtag_to_occurences_and_average_likes.items():
                number_of_posts_with_this_hashtag, likes = data
                average_likes = int(likes) / number_of_posts_with_this_hashtag
                dict_writer.writerow(
                    {
                        "hashtag": hashtag,
                        "average_likes": average_likes,
                        "number_of_posts_with_this_hashtag": number_of_posts_with_this_hashtag,
                    }
                )


if __name__ == "__main__":
    posts_csv_data_creator = hashtagAnalyser()
    posts_csv_data_creator.create_hashtag_likes_csv()
