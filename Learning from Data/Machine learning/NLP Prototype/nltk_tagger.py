import csv
import nltk
import pandas as pd

# TODO rule of thumb: for each feature at least 10 data points
class NLTKTagger:
    @staticmethod
    def create_csv_with_tags(id_of_post_to_data):
        with open("id_to_tags.csv", "w") as prototype_correlation_csv_file:
            fieldnames = [
                "id_of_post",
                "NN",
                "NNP",
                "JJ",
                "VBZ",
                "VBP",
                "RB",
                "VBD",
                "IN",
                "NNS",
                "LS",
                "TO",
                "VBN",
                "WP",
                "UH",
                "VBG",
                "DT",
                "PRP",
                "WP$",
                "NNPS",
                "PRP$",
                "WDT",
                "RBR",
                "RBS",
                "FW",
                "RP",
                "JJR",
                "JJS",
                "PDT",
                "MD",
                "VB",
                "WRB",
                "EX",
                "SYM",
                "CC",
                "CD",
                "POS",
                "''",
                "(",
                ")",
                ".",
                ",",
                ":",
                "``",
                "$",
                "--",
                "#",
                "likes_of_post",
            ]

            writer = csv.DictWriter(
                prototype_correlation_csv_file, fieldnames=fieldnames
            )
            writer.writeheader()

            for id_of_post, values in id_of_post_to_data.items():
                likes_of_post, _, description_of_post = values

                tagged_text = nltk.pos_tag(
                    nltk.Text(nltk.word_tokenize(description_of_post))
                )
                tags_to_occurrences = dict()
                for word_with_tag in tagged_text:
                    if word_with_tag[1] in tags_to_occurrences:
                        tags_to_occurrences[word_with_tag[1]] += 1
                    else:
                        tags_to_occurrences[word_with_tag[1]] = 1

                dictionary_to_write = tags_to_occurrences
                dictionary_to_write["id_of_post"] = id_of_post
                dictionary_to_write["likes_of_post"] = likes_of_post

                writer.writerow(dictionary_to_write)

    @staticmethod
    def id_of_post_to_data() -> dict:
        with open("../marry_items.csv", newline="") as marry_csv_file:
            dict_reader = csv.DictReader(marry_csv_file)
            # Put CSV data in dict (ID: liked by)
            id_of_post_to_data = dict()
            for row in dict_reader:
                # print(row["id_of_post"], row["likes_of_post"], row["hashtags_of_post"], row["description_of_post"])
                id_of_post_to_data[row["id_of_post"]] = (
                    row["likes_of_post"],
                    row["hashtags_of_post"],
                    row["description_of_post"],
                )

        return id_of_post_to_data


if __name__ == "__main__":
    nltk_tagger = NLTKTagger()
    nltk_tagger.create_csv_with_tags(nltk_tagger.id_of_post_to_data())
