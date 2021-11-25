import csv
import re
from learning_from_data.machine_learning.cluster_analysis.leveshtein_cluster import (
    levenshtein_distance_calculator,
)

CLUSTERING_INTERPRETATION_RESULTS_CSV = "/home/stefan/Knowledge/Bachelor-thesis/learning_from_data/new_clusters_interpretation/clustering_interpretation_results.csv"


# TODO for all clusters
class silhouetteScorer:
    def __init__(self):
        self.cluster_to_hashtags_and_scores = dict()
        self.levenshtein_distance_calculator = (
            levenshtein_distance_calculator.LevenshteinDistanceCalculator()
        )

    def load_data(self):
        with open(
            CLUSTERING_INTERPRETATION_RESULTS_CSV, newline=""
        ) as clustering_interpretation_reulsts_csv_file:
            dict_reader = csv.DictReader(clustering_interpretation_reulsts_csv_file)

            for row in dict_reader:
                cluster_name = row["community_clusters"]
                used_hashtags = row["hashtags_of_community_clusters"].split(",")
                calculated_score = row["score_of_community_clusters"]
                hashtags = list()

                for hashtag in used_hashtags:
                    hashtag = re.sub(r"\W+", "", hashtag)
                    if hashtag == "" or hashtag == " ":
                        continue
                    hashtags.append(hashtag)

                self.cluster_to_hashtags_and_scores[cluster_name] = (
                    hashtags,
                    calculated_score,
                    0,
                )

    def calculate_scores(self):
        for cluster, (
            hashtags,
            score,
            _,
        ) in self.cluster_to_hashtags_and_scores.items():
            intra_cluster_distance = self.intra_cluster_distance(hashtags)
            mean_nearest_cluster_distance = self.mean_nearest_cluster_distance(
                hashtags, cluster
            )
            silhouette_score = self.silhouette_score(
                intra_cluster_distance, mean_nearest_cluster_distance
            )

            self.cluster_to_hashtags_and_scores[cluster] = (
                hashtags,
                score,
                silhouette_score,
            )

    # Average distance of the hashtags inside of the cluster -> we use the element on position 0 as centroid.
    def intra_cluster_distance(self, hashtags):
        centroid = hashtags[0]
        total_distance = 0

        for hashtag in hashtags:
            if hashtag == centroid:
                continue
            total_distance += (
                self.levenshtein_distance_calculator.levenshtein_distance_of_words(
                    centroid, hashtag
                )
            )

        # -1 because the centroid is excluded on average distances.
        average_distance = total_distance / (len(hashtags) - 1)
        return average_distance

    # Take the min distance from centroid to all clusters
    def mean_nearest_cluster_distance(self, initial_cluster_hashtags, cluster):
        centroid = initial_cluster_hashtags[0]
        min_distance = float("inf")

        for cluster_name, (
            hashtags,
            score,
            _,
        ) in self.cluster_to_hashtags_and_scores.items():
            total_distance = 0

            if cluster_name == cluster:
                continue
            for hashtag in hashtags:
                total_distance += (
                    self.levenshtein_distance_calculator.levenshtein_distance_of_words(
                        centroid, hashtag
                    )
                )
            average_distance = total_distance / (len(hashtags) - 1)

            if average_distance < min_distance:
                min_distance = average_distance

        return min_distance

    @staticmethod
    def silhouette_score(intra_cluster_distance, mean_nearest_cluster_distance):
        # (mean_nearest_cluster_distance - intra_cluster_distance) / max(intra_cluster_distance, mean_nearest_cluster_distance)
        a = intra_cluster_distance
        b = mean_nearest_cluster_distance
        return (b - a) / max(a, b)

    def safe_interpretation_in_csv(self):
        with open(
            "community_clusters_silhouette_score.csv", "w", newline=""
        ) as clustering_interpretation_results:
            fieldnames = [
                "community_clusters",
                "hashtags_of_community_clusters",
                "score_of_community_clusters",
                "silhouette_score_of_community_cluster",
            ]
            dict_writer = csv.DictWriter(
                clustering_interpretation_results, fieldnames=fieldnames
            )
            dict_writer.writeheader()

            for community_cluster, (
                community_hashtags,
                community_score,
                silhouette_score,
            ) in self.cluster_to_hashtags_and_scores.items():
                dict_writer.writerow(
                    {
                        "community_clusters": community_cluster,
                        "hashtags_of_community_clusters": community_hashtags,
                        "score_of_community_clusters": community_score,
                        "silhouette_score_of_community_cluster": silhouette_score,
                    }
                )


if __name__ == "__main__":
    silhouette_scorer = silhouetteScorer()
    silhouette_scorer.load_data()
    silhouette_scorer.calculate_scores()
    silhouette_scorer.safe_interpretation_in_csv()
