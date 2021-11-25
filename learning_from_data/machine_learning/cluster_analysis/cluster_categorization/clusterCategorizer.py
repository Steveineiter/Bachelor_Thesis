import csv

# Input:
CLUSTER_FILE = "/home/stefan/Knowledge/Bachelor-thesis/Learning from Data/machine_learning/cluster_analysis/cluster_categorization/levenshtein_clusters.csv"

# Constants
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

class clusterCategorizer:
    def create_categorization(self):
        cluster_to_hashtags = self.cluster_to_hashtags()
        clusters_to_personas_and_hashtags = self.usernames_to_personas_and_hashtags(
            cluster_to_hashtags
        )
        self.safe_data_in_csv(clusters_to_personas_and_hashtags)

    @staticmethod
    def cluster_to_hashtags():
        cluster_to_hashtags = dict()
        with open(CLUSTER_FILE, "r", newline="") as clusters_csv_file:
            dict_reader = csv.DictReader(clusters_csv_file)

            for row in dict_reader:
                cluster_to_hashtags[row["cluster"]] = row["used_hashtags"]

            for username, hashtags in cluster_to_hashtags.items():
                hashtags = hashtags.split("'")[1:]
                hashtags = [item for item in hashtags if item != ", "]
                for index in range(len(hashtags)):
                    hashtags[index] = "#" + hashtags[index].strip()
                cluster_to_hashtags[username] = hashtags

        return cluster_to_hashtags

    def usernames_to_personas_and_hashtags(self, usernames_to_hashtags):
        usernames_to_personas_and_hashtags = dict()
        for username, hashtags in usernames_to_hashtags.items():
            hashtags_of_user_without_duplicates = list(dict.fromkeys(hashtags))
            like_linda = self.like_persona(hashtags_of_user_without_duplicates, HASHTAGS_LINDA)
            like_karl_peter = self.like_persona(hashtags_of_user_without_duplicates, HASHTAGS_KARL_PETER)
            like_sandy = self.like_persona(hashtags_of_user_without_duplicates, HASHTAGS_SANDY)
            like_kevin = self.like_persona(hashtags_of_user_without_duplicates, HASHTAGS_KEVIN)
            like_martin = self.like_persona(hashtags_of_user_without_duplicates, HASHTAGS_MARTIN)
            like_claudia = self.like_persona(hashtags_of_user_without_duplicates, HASHTAGS_CLAUDIA)

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
    def like_persona(hashtags_of_cluster, hashtags_of_persona):
        same_hashtags_count = 0

        for hashtag in hashtags_of_cluster:
            if hashtag in hashtags_of_persona:
                same_hashtags_count += 1

        return round((same_hashtags_count / len(hashtags_of_persona)) * 100, 2)

    @staticmethod
    def safe_data_in_csv(usernames_to_personas_and_hashtags):
        # Safe dict in CSV with columns Person, counter
        with open(
                "cluster_categorization.csv", "w", newline=""
        ) as persona_categorization_csv_file:
            fieldnames = [
                "username",
                "like_linda",
                "like_karl_peter",
                "like_sandy",
                "like_kevin",
                "like_martin",
                "like_claudia",
                "used_hashtags",
            ]
            dict_writer = csv.DictWriter(
                persona_categorization_csv_file, fieldnames=fieldnames
            )

            dict_writer.writeheader()
            for (
                    username,
                    liked_posts_count_and_id,
            ) in usernames_to_personas_and_hashtags.items():
                (
                    like_linda,
                    like_karl_peter,
                    like_sandy,
                    like_kevin,
                    like_martin,
                    like_claudia,
                    used_hashtags,
                ) = liked_posts_count_and_id
                dict_writer.writerow(
                    {
                        "username": username,
                        "like_linda": str(like_linda) + "%",
                        "like_karl_peter": str(like_karl_peter) + "%",
                        "like_sandy": str(like_sandy) + "%",
                        "like_kevin": str(like_kevin) + "%",
                        "like_martin": str(like_martin) + "%",
                        "like_claudia": str(like_claudia) + "%",
                        "used_hashtags": str(used_hashtags),
                    }
                )


if __name__ == "__main__":
    cluster_categorizer = clusterCategorizer()
    cluster_categorizer.create_categorization()
