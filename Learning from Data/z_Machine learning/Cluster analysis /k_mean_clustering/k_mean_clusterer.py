# Idee:
# 1. get K random hashtags
# 2. calculate levenshtein disctances to those centroids
# 3. cluster it up
# 4. calculate the best new centroid in cluster
#    (which hashtag has the smallest total number of levenshtein distances) # TODO Ponder if necessary
# 5. Repeat 2-5 until the centroid stays the same or MAX_ITERATIONS is reached
# 6. Return clusters aka personas

import csv
import random
from nltk.corpus import stopwords
from levenshtein_distance_calculator import (
    LevenshteinDistanceCalculator,
)  # Import from levenshtein cluster didn't work

MAX_HASHTAGS = 200
MAX_ITERATION = 5
K = 100


class Cluster:
    def __init__(self, centroid):
        self.centroid = centroid
        self.members = list()

    def get_centroid(self):
        return self.centroid

    def get_members(self):
        return self.members

    def add_member(self, member):
        self.members.append(member)

    def new_centroid(self, centroid):
        self.centroid = centroid

    def clear_members(self):
        self.members.clear()


class KMeanClusterer:
    def __init__(self, list_of_hashtags, k):
        self.list_of_hashtags = list_of_hashtags
        self.k = k
        self.clusters = list()
        self.current_centroids = list()
        self.levenshtein_distance_calculator = LevenshteinDistanceCalculator()

    def perform_clustering(self):
        self.initiate_centroids()
        self.assign_member_to_cluster()

        # Neuen centroids
        # fuer alle cluster, finde wort das in summe an wenigsten distance hat.
        has_centroids_changed = True
        current_iteration = 0
        while has_centroids_changed and current_iteration < MAX_ITERATION:
            print("Current iteration: ", current_iteration + 1)
            old_centroids = self.current_centroids
            self.calculate_new_centroids()
            # if new centroids == old centroids:
            #    break
            self.assign_member_to_cluster()
            has_centroids_changed = False
            for centroid in self.current_centroids:
                if centroid not in old_centroids:
                    has_centroids_changed = True
            current_iteration += 1

    def initiate_centroids(self):
        for index in range(self.k):
            random_centroid_index = random.randint(0, len(self.list_of_hashtags) - 1)
            self.clusters.append(Cluster(self.list_of_hashtags[random_centroid_index]))
            self.current_centroids.append(self.list_of_hashtags[random_centroid_index])

    def assign_member_to_cluster(self):
        for element in self.list_of_hashtags:
            min_levenshtein_distance = float("inf")
            best_cluster = Cluster(None)
            if element in self.current_centroids:
                continue

            for cluster in self.clusters:
                current_levenshtein_distance = (
                    self.levenshtein_distance_calculator.levenshtein_distance_of_words(
                        cluster.get_centroid(), element
                    )
                )
                if current_levenshtein_distance < min_levenshtein_distance:
                    min_levenshtein_distance = current_levenshtein_distance
                    best_cluster = cluster
            best_cluster.add_member(element)

    def calculate_new_centroids(self):
        new_centroids = list()

        for cluster in self.clusters:
            min_distances_sum = self.sum_distance_of_current_centroid(cluster)
            best_member = cluster.get_centroid()

            for member in cluster.get_members():
                current_distance_sum = 0
                current_distance_sum += (
                    self.levenshtein_distance_calculator.levenshtein_distance_of_words(
                        member, cluster.get_centroid()
                    )
                )
                for member_to_compare in cluster.get_members():
                    if member == member_to_compare:
                        continue
                    current_distance_sum += self.levenshtein_distance_calculator.levenshtein_distance_of_words(
                        member, member_to_compare
                    )
                # TODO bei verlgeich dann sobald es > als minimum ist abbrechnen -> damit soltle es viel schneller sein
                if current_distance_sum >= min_distances_sum:
                    continue
                min_distances_sum = current_distance_sum
                best_member = member

            cluster.new_centroid(best_member)
            new_centroids.append(best_member)
            # derweil einfach imemr alle members wegwerfen,
            #   TODO performance imporve, cluster nur weg werfen wenn nicht gebraucht
            cluster.clear_members()

        self.current_centroids = new_centroids

    def sum_distance_of_current_centroid(self, cluster):
        sum_distance = 0
        for member in cluster.get_members():
            sum_distance += (
                self.levenshtein_distance_calculator.levenshtein_distance_of_words(
                    cluster.get_centroid(), member
                )
            )
        return sum_distance

    def print_clustering_result(self):
        for cluster in self.clusters:
            print("*" * 40)
            print(
                "Cluster Centroid: ",
                cluster.get_centroid(),
                "\nCluster members:",
                cluster.get_members(),
            )

    def safe_clusters_in_csv(self):
        with open("clustering_results.csv", "w", newline="") as clusters_csv_file:
            fieldnames = ["cluster", "centroid", "used_hashtags"]
            dict_writer = csv.DictWriter(clusters_csv_file, fieldnames=fieldnames)
            dict_writer.writeheader()

            counter = 1
            for cluster in self.clusters:
                members = cluster.members
                hashtags = members
                # hashtags = list()
                # for member in members:
                #     hashtags.append("#" + member)

                dict_writer.writerow(
                    {
                        "cluster": f"k mean cluster {counter}",
                        "centroid": cluster.get_centroid(),
                        "used_hashtags": hashtags,
                    }
                )
                counter += 1


class KMeanClusterAnalyser:
    def __init__(self):
        self.list_of_hashtags = list()
        self.index_to_word = dict()
        self.clusterer = None

    # Read csv and extract hashtags
    def hashtags_from_csv(self):
        with open("used_hashtags_all.csv", newline="") as used_hashtags_csv_file:
            dict_reader = csv.DictReader(used_hashtags_csv_file)
            hashtag_counter = 0
            all_stopwords = stopwords.words("english")

            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                hashtag = row["hashtag"].split("#")[1]
                if (
                    hashtag != ""
                    and hashtag != " "
                    and len(self.list_of_hashtags) < MAX_HASHTAGS
                ):
                    if hashtag not in all_stopwords:
                        self.list_of_hashtags.append(hashtag)
                        self.index_to_word[str(hashtag_counter)] = hashtag
                        hashtag_counter += 1

    def initiate_k_mean_clusters(self):
        self.clusterer = KMeanClusterer(self.list_of_hashtags, K)

    def perform_k_mean_clustering(self):
        self.clusterer.perform_clustering()

    def print_clustering_result(self):
        self.clusterer.print_clustering_result()

    def safe_clusters_in_csv(self):
        self.clusterer.safe_clusters_in_csv()


if __name__ == "__main__":
    cluster_analyser = KMeanClusterAnalyser()
    cluster_analyser.hashtags_from_csv()
    cluster_analyser.initiate_k_mean_clusters()
    cluster_analyser.perform_k_mean_clustering()
    cluster_analyser.print_clustering_result()
    cluster_analyser.safe_clusters_in_csv()
