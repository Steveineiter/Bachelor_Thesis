# 1. read CSV with users and used hashtags
# Create graph: if word got used together with another, increase weight of this edge
# remove edges with weight less then threshold
# make the same as on the levenshtein cluster
import csv
import re

from nltk.corpus import stopwords


# Constants
PERSONAS_WITH_HASHTAGS_CSV = "persona_categorization.csv"
SOURCE = 0
DESTINATION = 1
WEIGHT = 2

# Constants to adjust
THRESHOLD = 2  # if value is greater then this, add to graph.
MAXIMAL_ITEMS_PER_CLUSTER = 7  # Somehow if i use 8 it has sometimes 9 items. With 7 it works.


class Cluster:
    def __init__(self):
        self.edges = dict()
        self.elements = set()

    def add_to_cluster(self, source, destination, weight):
        self.edges[source, destination] = weight
        self.elements.add(source)  # Check this
        self.elements.add(destination)

    def is_edge_connected(self, source, destination):
        if source in self.elements or destination in self.elements:
            return True
        return False


class Graph:
    def __init__(self):
        self.edges = dict()

    def update_edge_of_graph(self, source, destination):
        if (destination, source) in self.edges:
            return
        else:
            if (source, destination) in self.edges:
                self.edges[(source, destination)] += 1
            else:
                self.add_new_edge(source, destination)

    # TODO Maybe do something against duplicates, eg now a->b and b->a are in graph.
    def add_new_edge(self, source, destination):
        self.edges[(source, destination)] = 1

    def delete_elements_with_too_small_weight(self):
        new_edges = dict()
        for key, weight in self.edges.items():
            if weight < THRESHOLD:
                continue
            else:
                new_edges[key] = weight

        self.edges = new_edges


class CommunitiesClusterAnalyser:
    def __init__(self):
        self.hashtag_groups = list()
        self.graph = Graph()
        self.clusters = None

    # Read csv and extract hashtags
    def hashtags_from_csv(self):
        with open(PERSONAS_WITH_HASHTAGS_CSV, newline="") as used_hashtags_csv_file:
            dict_reader = csv.DictReader(used_hashtags_csv_file)
            hashtag_counter = 0
            all_stopwords = stopwords.words("english")

            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                list_of_hashtags = list()
                hashtags = row["used_hashtags"].split("#")
                for hashtag in hashtags:
                    hashtag = re.sub(r'\W+', '', hashtag)
                    if (
                            hashtag == ""
                            or hashtag == " "
                    ):
                        continue

                    if hashtag not in all_stopwords:
                        list_of_hashtags.append(hashtag)
                        hashtag_counter += 1
                self.hashtag_groups.append(list_of_hashtags)

    def create_graph(self):
        for hashtag_group in self.hashtag_groups:
            for hashtag in hashtag_group:
                for hashtag_to_link in hashtag_group:
                    if hashtag == hashtag_to_link:
                        continue

                    self.graph.update_edge_of_graph(hashtag, hashtag_to_link)

    def print_graph(self):
        for (source, destination), weight in self.graph.edges.items():
            if weight > 2:
                print(source, destination, ": ", weight)

    def delete_elements_with_too_small_weight(self):
        self.graph.delete_elements_with_too_small_weight()

    def create_cluster(self):
        clusters = list()

        for (source, destination), weight in self.graph.edges.items():
            is_in_a_cluster = False
            if len(clusters) == 0:
                new_cluster = Cluster()
                new_cluster.add_to_cluster(source, destination, weight)
                clusters.append(new_cluster)

            for cluster in clusters:
                if len(cluster.edges) >= MAXIMAL_ITEMS_PER_CLUSTER:
                    continue
                if cluster.is_edge_connected(source, destination):
                    cluster.add_to_cluster(source, destination, weight)
                    is_in_a_cluster = True
                    break

            if not is_in_a_cluster:
                new_cluster = Cluster()
                new_cluster.add_to_cluster(source, destination, weight)
                clusters.append(new_cluster)

        self.clusters = clusters

    def safe_clusters_in_csv(self):
        with open("clustering_results.csv", "w", newline="") as clusters_csv_file:
            fieldnames = ["cluster", "used_hashtags"]
            dict_writer = csv.DictWriter(
                clusters_csv_file, fieldnames=fieldnames
            )
            dict_writer.writeheader()

            counter = 1
            for cluster in self.clusters:
                elements = cluster.elements

                dict_writer.writerow(
                    {
                        "cluster": f"community cluster {counter}",
                        "used_hashtags": elements
                    }
                )
                counter += 1


if __name__ == "__main__":
    cluster_analyser = CommunitiesClusterAnalyser()
    cluster_analyser.hashtags_from_csv()
    cluster_analyser.create_graph()
    cluster_analyser.delete_elements_with_too_small_weight()
    cluster_analyser.create_cluster()
    print("safe clusters in csv")
    cluster_analyser.safe_clusters_in_csv()
