# Bekomme wieder alle hashtags von usern
# Bekomem alle clusters, aber aufgeteilt in enrica,levenshtein, kmean
# Berechne fuer jeden cluster einen score

# Score = pro hashtag das cluster und eine person haben += 1, am ende Score * number_of_hashtags_factor

# number_of_hashtags_factor = pro wort weniger als 20 x% mehr -> wenn ein cluster nur 10 worte hat aber gleich gut
# performed wie einer mit 20, soll er besser sein (zB bei x=5% -> cluster haben beide score von 100, 10 wort cluster
# hat dannach score von 150 (10(differenz 20 und 10)*5%)

# Gib top cluster noch in eigener column aus

# CSV: Enrica_cluster | score_of_enrica_cluster | k_mean | k_mean_score | levenshtein | levenshtein_score | Best_cluster | best_clusters_score


import csv
import re

from nltk.corpus import stopwords

# Constants to adjust
USED_HASHTAGS_CSV_PATH = "/home/stefan/Knowledge/Bachelor-thesis/Learning from Data/new_clusters_interpretation/data/used_hashtags.csv"
COMMUNITY_CLUSTER_RESULTS = "/home/stefan/Knowledge/Bachelor-thesis/Learning from Data/new_clusters_interpretation/data/community_clustering_results.csv"
K_MEAN_CLUSTER_RESULTS = "/home/stefan/Knowledge/Bachelor-thesis/Learning from Data/new_clusters_interpretation/data/k_mean_clustering_results.csv"
LEVENSHTEIN_CLUSTER_RESULTS = "/home/stefan/Knowledge/Bachelor-thesis/Learning from Data/new_clusters_interpretation/data/levenshtein_clustering_results.csv"
# Determines how much a cluster should be rewarded if it has fewer hashtags.
NUMBER_OF_HASHTAGS_FACTOR = 0.05
NUMBER_OF_HASHTAGS_BASELINE = 20
# For cases where a hashtag gets used all the time, eg "Graz", # so that it doesnt get overwhelming.
MAXIMUM_SCORE_PER_HASHTAG = 1  # TODO make it dynamic, eg mean of all hashtags.
NUMBER_OF_BEST_CLUSTERS = 20

# Constants


class persona_Interpreter:
    def __init__(self):
        self.used_hashtags_to_occurrences = dict()
        self.community_clusters = dict()
        self.k_mean_clusters = dict()
        self.levenshtein_clusters = dict()
        self.best_clusters_list = dict()

    def load_data(self):
        self.read_used_hashtags_csv()
        self.read_cluster_csv(COMMUNITY_CLUSTER_RESULTS, self.community_clusters)
        self.read_cluster_csv(K_MEAN_CLUSTER_RESULTS, self.k_mean_clusters)
        self.read_cluster_csv(LEVENSHTEIN_CLUSTER_RESULTS, self.levenshtein_clusters)

    def calculate_scores(self):
        self.calculate_score_of_clusters(self.community_clusters)
        self.calculate_score_of_clusters(self.k_mean_clusters)
        self.calculate_score_of_clusters(self.levenshtein_clusters)

    def best_clusters(self):
        all_clusters = dict(self.community_clusters, **self.k_mean_clusters)
        all_clusters.update(self.levenshtein_clusters)
        all_clusters_sorted = sorted(
            all_clusters.items(), key=lambda item: item[1][1], reverse=True
        )
        self.best_clusters_list = dict(all_clusters_sorted[:NUMBER_OF_BEST_CLUSTERS])

    def calculate_score_of_clusters(self, clusters: dict):
        for cluster, hashtags in clusters.items():
            score = 0

            for hashtag in hashtags:
                if hashtag in self.used_hashtags_to_occurrences.keys():
                    score += min(
                        MAXIMUM_SCORE_PER_HASHTAG,
                        int(self.used_hashtags_to_occurrences[hashtag]),
                    )

            difference = NUMBER_OF_HASHTAGS_BASELINE - len(hashtags)
            score *= 1 + (difference * NUMBER_OF_HASHTAGS_FACTOR)

            clusters[cluster] = (hashtags, score)

    def read_used_hashtags_csv(self):
        with open(USED_HASHTAGS_CSV_PATH, newline="") as used_hashtags_csv_file:
            dict_reader = csv.DictReader(used_hashtags_csv_file)
            all_stopwords = stopwords.words("english")

            for row in dict_reader:
                hashtag = row["hashtag"].split("#")[1]
                number_of_users_who_used_it = row["number_of_users_who_used_it"]
                if hashtag != "" and hashtag != " ":
                    if hashtag in all_stopwords:
                        continue

                    self.used_hashtags_to_occurrences[
                        hashtag
                    ] = number_of_users_who_used_it

    @staticmethod
    def read_cluster_csv(csv_file, cluster_to_hashtags):
        with open(csv_file, newline="") as cluster_csv_file:
            dict_reader = csv.DictReader(cluster_csv_file)

            for row in dict_reader:
                cluster = row["cluster"]
                used_hashtags = row["used_hashtags"].split(",")
                hashtags = list()
                for hashtag in used_hashtags:
                    hashtag = re.sub(r"\W+", "", hashtag)
                    if hashtag == "" or hashtag == " ":
                        continue
                    hashtags.append(hashtag)
                cluster_to_hashtags[cluster] = hashtags

    def safe_interpretation_in_csv(self):
        with open(
            "clustering_interpretation_results.csv", "w", newline=""
        ) as clustering_interpretation_results:
            fieldnames = [
                "community_clusters",
                "hashtags_of_community_clusters",
                "score_of_community_clusters",
                "k_mean_clusters",
                "hashtags_of_k_mean_clusters",
                "score_of_k_mean_clusters",
                "levenshtein_clusters",
                "hashtags_of_levenshtein_clusters",
                "score_of_levenshtein_clusters",
                "best_clusters",
                "hashtags_of_best_clusters",
                "score_of_best_clusters",
            ]
            dict_writer = csv.DictWriter(
                clustering_interpretation_results, fieldnames=fieldnames
            )
            dict_writer.writeheader()

            community_clusters = self.cluster_list(self.community_clusters)
            k_mean_clusters = self.cluster_list(self.k_mean_clusters)
            levenshtein_clusters = self.cluster_list(self.levenshtein_clusters)
            best_clusters = self.cluster_list(self.best_clusters_list)

            for i in range(len(community_clusters)):
                community_cluster = community_clusters[i][0]
                community_hashtags = community_clusters[i][1]
                community_score = community_clusters[i][2]

                if i < len(k_mean_clusters):
                    k_mean_cluster = k_mean_clusters[i][0]
                    k_mean_cluster_hashtags = k_mean_clusters[i][1]
                    k_mean_cluster_score = k_mean_clusters[i][2]
                else:
                    k_mean_cluster = None
                    k_mean_cluster_hashtags = None
                    k_mean_cluster_score = None

                if i < len(levenshtein_clusters):
                    levenshtein_cluster = levenshtein_clusters[i][0]
                    levenshtein_cluster_hashtags = levenshtein_clusters[i][1]
                    levenshtein_cluster_score = levenshtein_clusters[i][2]
                else:
                    levenshtein_cluster = None
                    levenshtein_cluster_hashtags = None
                    levenshtein_cluster_score = None

                if i < len(best_clusters):
                    best_cluster = best_clusters[i][0]
                    best_cluster_hashtags = best_clusters[i][1]
                    best_cluster_score = best_clusters[i][2]
                else:
                    best_cluster = None
                    best_cluster_hashtags = None
                    best_cluster_score = None

                dict_writer.writerow(
                    {
                        "community_clusters": community_cluster,
                        "hashtags_of_community_clusters": community_hashtags,
                        "score_of_community_clusters": community_score,
                        "k_mean_clusters": k_mean_cluster,
                        "hashtags_of_k_mean_clusters": k_mean_cluster_hashtags,
                        "score_of_k_mean_clusters": k_mean_cluster_score,
                        "levenshtein_clusters": levenshtein_cluster,
                        "hashtags_of_levenshtein_clusters": levenshtein_cluster_hashtags,
                        "score_of_levenshtein_clusters": levenshtein_cluster_score,
                        "best_clusters": best_cluster,
                        "hashtags_of_best_clusters": best_cluster_hashtags,
                        "score_of_best_clusters": best_cluster_score,
                    }
                )

    @staticmethod
    def cluster_list(clusters):
        clusters_list = list()
        for cluster_index, (hashtags, score) in clusters.items():
            clusters_list.append((cluster_index, hashtags, score))

        return clusters_list


if __name__ == "__main__":
    persona_interpreter = persona_Interpreter()
    persona_interpreter.load_data()
    persona_interpreter.calculate_scores()
    persona_interpreter.best_clusters()
    persona_interpreter.safe_interpretation_in_csv()
