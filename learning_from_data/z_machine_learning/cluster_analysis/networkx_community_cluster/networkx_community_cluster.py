import csv
import re

import networkx as nx


# 1. get all hashtags per user as unicate (eg user has used "foo, foo, bar" => "foo, bar")
# 2. create a dict between all words, eg foo - bar weight = 1, if another user also used those two weight = 2
# 3. build graph out of that
import numpy as np
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from networkx.algorithms.community import greedy_modularity_communities
from sklearn.metrics import silhouette_score

PERSONAS_WITH_HASHTAGS_CSV = "persona_categorization.csv"


class NetworkXCommunityClusterAnalyser:
    def __init__(self):
        self.graph = nx.Graph()
        self.hashtag_groups = list()
        self.communities = list()
        self.silhouette_score = int()

    def hashtags_from_csv(self):
        with open(PERSONAS_WITH_HASHTAGS_CSV, newline="") as used_hashtags_csv_file:
            dict_reader = csv.DictReader(used_hashtags_csv_file)
            all_stopwords = stopwords.words("english")

            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                list_of_hashtags = list()
                hashtags = row["used_hashtags"].split("#")
                for hashtag in hashtags:
                    hashtag = re.sub(r"\W+", "", hashtag)
                    if hashtag == "" or hashtag == " ":
                        continue

                    if hashtag not in all_stopwords:
                        list_of_hashtags.append(hashtag)
                self.hashtag_groups.append(list_of_hashtags)

    def create_graph(self):
        for together_used_hashtags in self.hashtag_groups:
            for i in range(len(together_used_hashtags)):
                for j in range(i + 1, len(together_used_hashtags)):
                    try:
                        self.graph[together_used_hashtags[i]][
                            together_used_hashtags[j]
                        ]["weight"] = (
                            self.graph[together_used_hashtags[i]][
                                together_used_hashtags[j]
                            ]["weight"]
                            + 1
                        )
                    except KeyError:
                        self.graph.add_edge(
                            together_used_hashtags[i],
                            together_used_hashtags[j],
                            weight=1,
                        )

    def create_communities_and_silhouette_score(self):
        self.communities = list(greedy_modularity_communities(self.graph))
        index_to_hashtag = dict()
        counter = 0
        for node, _ in self.graph.adj.items():
            index_to_hashtag[counter] = node
            counter += 1
        graph_nodes = [i for i in index_to_hashtag]
        graph_nodes = np.array(graph_nodes)
        labels = list()
        for node in graph_nodes:
            for i in range(len(self.communities)):
                if index_to_hashtag[node] in self.communities[i]:
                    labels.append(i)
                    continue
        self.silhouette_score = silhouette_score(graph_nodes.reshape(-1, 1), labels)

    def safe_clusters_in_csv(self):
        with open("clustering_results.csv", "w", newline="") as clusters_csv_file:
            fieldnames = ["cluster", "used_hashtags", "silhouette_score"]
            dict_writer = csv.DictWriter(clusters_csv_file, fieldnames=fieldnames)
            dict_writer.writeheader()

            counter = 1
            for cluster in self.communities:
                hashtags = list()
                for hashtag in cluster:
                    hashtags.append(hashtag)

                dict_writer.writerow(
                    {
                        "cluster": f"community cluster {counter}",
                        "used_hashtags": hashtags,
                        "silhouette_score": self.silhouette_score,
                    }
                )
                counter += 1


if __name__ == "__main__":
    cluster_analyser = NetworkXCommunityClusterAnalyser()
    cluster_analyser.hashtags_from_csv()
    cluster_analyser.create_graph()
    cluster_analyser.create_communities_and_silhouette_score()
    cluster_analyser.safe_clusters_in_csv()
