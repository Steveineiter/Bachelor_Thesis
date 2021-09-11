import csv
import glob
import re
from collections import defaultdict

HASHTAGS_LINDA = (
    "#local #cooking #bouldering #sports #lesssugar #traveling #healthy "
    "#grazblogger #happyme #backen #foodblogger #backenmachtglücklich".split(" ")
)
HASHTAGS_KARL_PETER = "#programming #memes #techlife #food #working #coffein".split(" ")
HASHTAGS_SANDY = (
    "#party #music #drinking #creativity #illustration #design #celebration".split(" ")
)
HASHTAGS_KEVIN = (
    "#cooking #food #music #traveling #dog #dogslover #photography #art ".split(" ")
)
HASHTAGS_MARTIN = "#family #familytime #friends #father #fatherandson #biking".split(
    " "
)
HASHTAGS_CLAUDIA = (
    "#family #mum #local #familienleben #decoration #handmade #nature".split(" ")
)

CLUSER_INTERPRETATION_CSV = "/home/stefan/Knowledge/Bachelor-thesis/learning_from_data/personas_with_hashtags/twitter/clusters/clustering_interpretation_max_score_5_results.csv"


class personaCategorizer:
    def __init__(self):
        self.top_20_clusters = self.top_20_clusters()

    def create_categorization(self):
        usernames_to_hashtags = self.usernames_to_hashtags()
        usernames_to_clusters = self.usernames_to_clusters(usernames_to_hashtags)
        usernames_to_personas_and_hashtags = self.usernames_to_personas_and_hashtags(
            usernames_to_hashtags
        )
        usernames_to_data = self.merge_dicts(
            usernames_to_personas_and_hashtags, usernames_to_clusters
        )

        self.safe_data_in_csv(usernames_to_data)

    @staticmethod
    def usernames_to_hashtags():
        usernames_to_hashtags = dict()
        files = glob.glob("data" + "/*.csv", recursive=True)
        for file in files:
            parts_of_path = file.split("_")
            username = parts_of_path[0].split("/")[1]  # To get rid of data/

            with open(file, newline="") as twitter_user_csv_file:
                dict_reader = csv.DictReader(twitter_user_csv_file)
                for row in dict_reader:
                    if username in usernames_to_hashtags.keys():
                        usernames_to_hashtags[username] += [
                            row["Text"],
                            row["Embedded_text"],
                        ]
                    else:
                        usernames_to_hashtags[username] = [
                            row["Text"],
                            row["Embedded_text"],
                        ]

        for username, text_of_posts in usernames_to_hashtags.items():
            used_hashtags = list()
            for text in text_of_posts:
                hashtags = re.findall(r"#\w+", text)
                for hashtag in hashtags:
                    used_hashtags.append(hashtag)
            usernames_to_hashtags[username] = used_hashtags

        return usernames_to_hashtags

    def usernames_to_personas_and_hashtags(self, usernames_to_hashtags):
        usernames_to_personas_and_hashtags = dict()
        for username, hashtags in usernames_to_hashtags.items():
            hashtags_of_user_without_duplicates = list(dict.fromkeys(hashtags))
            like_linda = self.like_persona(
                hashtags_of_user_without_duplicates, HASHTAGS_LINDA
            )
            like_karl_peter = self.like_persona(
                hashtags_of_user_without_duplicates, HASHTAGS_KARL_PETER
            )
            like_sandy = self.like_persona(
                hashtags_of_user_without_duplicates, HASHTAGS_SANDY
            )
            like_kevin = self.like_persona(
                hashtags_of_user_without_duplicates, HASHTAGS_KEVIN
            )
            like_martin = self.like_persona(
                hashtags_of_user_without_duplicates, HASHTAGS_MARTIN
            )
            like_claudia = self.like_persona(
                hashtags_of_user_without_duplicates, HASHTAGS_CLAUDIA
            )

            usernames_to_personas_and_hashtags[username] = (
                like_linda,
                like_karl_peter,
                like_sandy,
                like_kevin,
                like_martin,
                like_claudia,
                hashtags_of_user_without_duplicates,
            )

        return usernames_to_personas_and_hashtags

    @staticmethod
    def like_persona(hashtags_of_user, hashtags_of_persona):
        same_hashtags_count = 0
        hashtags_of_persona_lower = list()
        hashtags_of_user_lower = list()

        for hashtag in hashtags_of_persona:
            hashtags_of_persona_lower.append(hashtag.lower())
        for hashtag in hashtags_of_user:
            hashtags_of_user_lower.append(hashtag.lower())

        for hashtag in hashtags_of_user_lower:
            if hashtag in hashtags_of_persona_lower:
                same_hashtags_count += 1

        return round((same_hashtags_count / len(hashtags_of_persona)) * 100, 2)

    def usernames_to_clusters(self, usernames_to_hashtags):
        usernames_to_clusters = dict()

        for username, hashtags in usernames_to_hashtags.items():
            best_cluster_top_20 = dict()
            best_cluster_top_20_max_score = float("-inf")

            hashtags_of_user_without_duplicates = list(dict.fromkeys(hashtags))
            for top_20_cluster in self.top_20_clusters.items():
                current_score = self.like_persona(
                    hashtags_of_user_without_duplicates, top_20_cluster[1]
                )
                if current_score > best_cluster_top_20_max_score:
                    best_cluster_top_20_max_score = current_score
                    best_cluster_top_20 = (
                        top_20_cluster[0],
                        best_cluster_top_20_max_score,
                    )

            usernames_to_clusters[username] = best_cluster_top_20

        return usernames_to_clusters

    @staticmethod
    def top_20_clusters():
        top_20_clusters = dict()
        with open(CLUSER_INTERPRETATION_CSV, newline="") as twitter_user_csv_file:
            dict_reader = csv.DictReader(twitter_user_csv_file)
            for row in dict_reader:
                cluster = row["best_clusters"]
                if not cluster:
                    break
                used_hashtags = row["hashtags_of_best_clusters"].split(",")
                hashtags = list()
                for hashtag in used_hashtags:
                    hashtag = re.sub(r"\W+", "", hashtag)
                    if hashtag == "" or hashtag == " ":
                        continue
                    hashtags.append("#" + hashtag)
                top_20_clusters[cluster] = hashtags

        return top_20_clusters

    @staticmethod
    def merge_dicts(dict_one, dict_two):
        default_dictionary = defaultdict(list)

        for dictionary in (dict_one, dict_two):
            for key, value in dictionary.items():
                default_dictionary[key].append(value)

        return default_dictionary

    @staticmethod
    def safe_data_in_csv(usernames_to_data):
        # Safe dict in CSV with columns Person, counter
        with open(
            "persona_categorization.csv", "w", newline=""
        ) as persona_categorization_csv_file:
            fieldnames = [
                "username",
                "like_linda",
                "like_karl_peter",
                "like_sandy",
                "like_kevin",
                "like_martin",
                "like_claudia",
                "like_best_cluster_of_all",
                "like_best_cluster_of_top_20",
                "used_hashtags",
            ]
            dict_writer = csv.DictWriter(
                persona_categorization_csv_file, fieldnames=fieldnames
            )
            dict_writer.writeheader()

            score_of_cluster = 0
            score_of_old_persona = 0
            for (
                username,
                data,
            ) in usernames_to_data.items():
                tuple_one, tuple_two = data
                if len(tuple_one) == 2:
                    cluster_data = tuple_one
                    persona_data = tuple_two
                if len(tuple_one) == 7:
                    persona_data = tuple_one
                    cluster_data = tuple_two

                (
                    like_linda,
                    like_karl_peter,
                    like_sandy,
                    like_kevin,
                    like_martin,
                    like_claudia,
                    used_hashtags,
                ) = persona_data

                dict_writer.writerow(
                    {
                        "username": username,
                        "like_linda": str(like_linda) + "%",
                        "like_karl_peter": str(like_karl_peter) + "%",
                        "like_sandy": str(like_sandy) + "%",
                        "like_kevin": str(like_kevin) + "%",
                        "like_martin": str(like_martin) + "%",
                        "like_claudia": str(like_claudia) + "%",
                        "like_best_cluster_of_all": None,  # TODO should we implement this? maybe worth for new clusters
                        "like_best_cluster_of_top_20": str(
                            f"{cluster_data[1]}%, Cluster: {cluster_data[0]}"
                        ),
                        "used_hashtags": str(used_hashtags),
                    }
                )
                score_of_cluster += cluster_data[1]
                score_of_old_persona += max(
                    like_linda,
                    like_karl_peter,
                    like_sandy,
                    like_kevin,
                    like_martin,
                    like_claudia,
                    )
            print(f"Aggregated % of cluster: {score_of_cluster:.2f}\n"
                  f"Aggregated % of best persona: {score_of_old_persona:.2f}")


if __name__ == "__main__":
    persona_categorizer = personaCategorizer()
    persona_categorizer.create_categorization()
