import csv

import nltk

nltk.download("stopwords")
from nltk.corpus import stopwords

import pandas as pd

from levenshtein_distance_calculator import LevenshteinDistanceCalculator
from kruskals_mst import Graph

# Constants to adjust
MAX_HASHTAGS = 100
WEIGHT_THRESHOLD = 2

# Constants
SOURCE = 0
DESTINATION = 1
WEIGHT = 2


class Cluster:
    def __init__(self):
        self.edges = list()
        self.elements = set()

    def add_to_cluster(self, edge: list):
        self.edges.append(edge)
        self.elements.add(edge[SOURCE])
        self.elements.add(edge[DESTINATION])

    def is_edge_connected(self, edge):
        source, destination, _ = edge
        if source in self.elements or destination in self.elements:
            return True
        return False


class ClusterAnalyser:
    def __init__(self):
        self.list_of_hashtags = list()
        self.levenshtein_matrix = None
        self.index_to_word = dict()
        self.minimum_spanning_tree = list()
        self.clusters = None

    # Read csv and extract hashtags
    def hashtags_from_csv(self):
        with open("used_hashtags.csv", newline="") as used_hashtags_csv_file:
            dict_reader = csv.DictReader(used_hashtags_csv_file)
            hashtag_counter = 0
            all_stopwords = stopwords.words("english")

            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                hashtag = row["hashtag"].split("#")[1]
                if hashtag != '' and hashtag != ' ' and len(self.list_of_hashtags) < MAX_HASHTAGS:
                    if hashtag not in all_stopwords:
                        self.list_of_hashtags.append(hashtag)
                        self.index_to_word[str(hashtag_counter)] = hashtag
                        hashtag_counter += 1

    # create levenshtein matrix
    def create_levenshtein_matrix(self):
        print("\n ***** Creating levenshtein matrix ***** \n")
        levenshtein_distance_calculator = LevenshteinDistanceCalculator()
        levenshtein_distance_calculator.levenshtein_distances_matrix(self.list_of_hashtags, is_safe_enabled=True)

    def levenshtein_matrix_from_csv(self, file):
        data_frame = pd.read_csv(file)
        self.levenshtein_matrix = data_frame.values

    # create MST
    def create_minimum_spanning_tree(self):
        number_of_hashtags = len(self.list_of_hashtags)
        graph = Graph((number_of_hashtags ** 2) - number_of_hashtags)
        for i in range(number_of_hashtags):
            for j in range(number_of_hashtags):
                if i != j:
                    graph.add_edge(i, j, self.levenshtein_matrix[i][j])
        graph.kruskal_minimum_spanning_tree()
        print("Removing duplicates")
        self.minimum_spanning_tree = self.spanning_tree_without_duplicates(graph.graph)

    @staticmethod
    def spanning_tree_without_duplicates(graph):
        cleaned_graph = list()

        # for edge in graph:
        #     is_already_in_cleaned_graph = False
        #
        #     if len(cleaned_graph) == 0:
        #         cleaned_graph.append(edge)
        #         continue
        #
        #     for cleaned_edge in cleaned_graph:
        #         if edge[SOURCE] == cleaned_edge[DESTINATION] and edge[DESTINATION] == cleaned_edge[SOURCE]:
        #             is_already_in_cleaned_graph = True
        #     if not is_already_in_cleaned_graph:
        #         cleaned_graph.append(edge)
        #
        # return cleaned_graph

        dictionary = {}
        for (source, destination, weight) in graph:
            if (destination, source, weight) in dictionary:
                continue
            else:
                dictionary[(source, destination, weight)] = (source, destination, weight)

        for edge in dictionary:
            cleaned_graph.append(list(edge))

        return cleaned_graph




    def delete_elements_with_too_large_weight(self, threshold):
        self.minimum_spanning_tree = [item for item in self.minimum_spanning_tree if item[WEIGHT] <= threshold]

    def create_cluster(self):
        clusters = list()

        for edge in self.minimum_spanning_tree:
            is_in_a_cluster = False
            if len(clusters) == 0:
                new_cluster = Cluster()
                new_cluster.add_to_cluster(self.minimum_spanning_tree[0])
                clusters.append(new_cluster)

            for cluster in clusters:
                if cluster.is_edge_connected(edge):
                    cluster.add_to_cluster(edge)
                    is_in_a_cluster = True
                    break

            if not is_in_a_cluster:
                new_cluster = Cluster()
                new_cluster.add_to_cluster(edge)
                clusters.append(new_cluster)

        self.clusters = clusters

    def safe_clusters_in_csv(self):
        with open("clusters.csv", "w", newline="") as clusters_csv_file:
            fieldnames = ["cluster", "used_hashtags"]
            dict_writer = csv.DictWriter(
                clusters_csv_file, fieldnames=fieldnames
            )
            dict_writer.writeheader()

            counter = 1
            for cluster in self.clusters:
                elements = cluster.elements
                hashtags = list()
                for element in elements:
                    hashtags.append(self.index_to_word[str(element)])

                dict_writer.writerow(
                    {
                        "cluster": f"cluster {counter}",
                        "used_hashtags": hashtags
                    }
                )
                counter += 1




if __name__ == "__main__":
    cluster_analyser = ClusterAnalyser()
    cluster_analyser.hashtags_from_csv()
    # cluster_analyser.create_levenshtein_matrix()
    cluster_analyser.levenshtein_matrix_from_csv("levenshtein_matrix.csv")
    print("Creating minimum spanning tree")
    cluster_analyser.create_minimum_spanning_tree()
    print("delete_elements_with_too_large_weight")
    cluster_analyser.delete_elements_with_too_large_weight(WEIGHT_THRESHOLD)
    print("create_cluster")
    cluster_analyser.create_cluster()
    print("safe clusters in csv")
    cluster_analyser.safe_clusters_in_csv()


# TODO find out how to use this output
# Output for 10: [
# [7, 8, 2], [8, 7, 2], [2, 7, 3], [2, 8, 3], [6, 8, 3], [7, 2, 3],
# [7, 9, 3], [8, 2, 3], [8, 6, 3], [9, 7, 3], [0, 9, 4], [2, 6, 4],
# [5, 8, 4], [6, 2, 4], [6, 7, 4], [7, 6, 4], [8, 5, 4], [9, 0, 4],
# [1, 4, 5], [1, 7, 5], [1, 9, 5], [2, 5, 5], [2, 9, 5], [4, 1, 5],
# [4, 9, 5], [5, 2, 5], [5, 7, 5], [6, 9, 5], [7, 1, 5], [7, 5, 5],
# [8, 9, 5], [9, 1, 5], [9, 2, 5], [9, 4, 5], [9, 6, 5], [9, 8, 5],
# [0, 1, 6], [0, 6, 6], [0, 7, 6], [1, 0, 6], [1, 6, 6], [4, 5, 6],
# [5, 4, 6], [5, 6, 6], [5, 9, 6], [6, 0, 6], [6, 1, 6], [6, 5, 6],
# [7, 0, 6], [9, 5, 6], [0, 2, 7], [0, 5, 7], [0, 8, 7], [1, 2, 7],
# [1, 5, 7], [1, 8, 7], [2, 0, 7], [2, 1, 7], [2, 4, 7], [3, 8, 7],
# [4, 2, 7], [4, 6, 7], [4, 7, 7], [4, 8, 7], [5, 0, 7], [5, 1, 7],
# [6, 4, 7], [7, 4, 7], [8, 0, 7], [8, 1, 7], [8, 3, 7], [8, 4, 7],
# [0, 4, 8], [1, 3, 8], [2, 3, 8], [3, 1, 8], [3, 2, 8], [3, 4, 8],
# [3, 5, 8], [3, 6, 8], [3, 7, 8], [4, 0, 8], [4, 3, 8], [5, 3, 8],
# [6, 3, 8], [7, 3, 8], [3, 9, 9], [9, 3, 9], [0, 3, 10], [3, 0, 10]]

# Output for 5: [
# [1, 4, 5], [4, 1, 5], [0, 1, 6], [1, 0, 6], [0, 2, 7], [1, 2, 7],
# [2, 0, 7], [2, 1, 7], [2, 4, 7], [4, 2, 7], [0, 4, 8], [1, 3, 8],
# [2, 3, 8], [3, 1, 8], [3, 2, 8], [3, 4, 8], [4, 0, 8], [4, 3, 8],
# [0, 3, 10], [3, 0, 10]
# ]