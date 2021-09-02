import csv

import pandas as pd

from levenshtein_distance_calculator import LevenshteinDistanceCalculator
from kruskals_mst import Graph

MAX_HASHTAGS = 10


class ClusterAnalyser:
    def __init__(self):
        self.list_of_hashtags = list()
        self.levenshtein_matrix = None

    # Read csv and extract hashtags
    def hashtags_from_csv(self):
        with open("used_hashtags.csv", newline="") as used_hashtags_csv_file:
            dict_reader = csv.DictReader(used_hashtags_csv_file)
            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                hashtag = row["hashtag"].split("#")[1]
                if hashtag != '' and hashtag != ' ' and len(self.list_of_hashtags) < MAX_HASHTAGS:
                    self.list_of_hashtags.append(hashtag)

    # create levenshtein matrix
    def create_levenshtein_matrix(self):
        print("\n ***** Creating levenshtein matrix ***** \n")
        levenshtein_distance_calculator = LevenshteinDistanceCalculator()
        levenshtein_distance_calculator.levenshtein_distances_matrix(self.list_of_hashtags, is_safe_enabled=True)

    def levenshtein_matrix_from_csv(self, file):
        data_frame = pd.read_csv(file)
        self.levenshtein_matrix = data_frame.values

    # create MST
    def create_MST(self):
        number_of_hashtags = len(self.list_of_hashtags)
        graph = Graph((number_of_hashtags ** 2) - number_of_hashtags)
        for i in range(number_of_hashtags):
            for j in range(number_of_hashtags):
                if i != j:
                    graph.add_edge(i, j, self.levenshtein_matrix[i][j])
        graph.kruskal_minimum_spanning_tree()
        return graph


if __name__ == "__main__":
    cluster_analyser = ClusterAnalyser()
    cluster_analyser.hashtags_from_csv()
    cluster_analyser.create_levenshtein_matrix()
    cluster_analyser.levenshtein_matrix_from_csv("levenshtein_matrix.csv")
    graph = cluster_analyser.create_MST()

# TODO find out how to use this output
# Output: [
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