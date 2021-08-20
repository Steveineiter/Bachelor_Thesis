import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import re
import nltk

nltk.download("stopwords")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split


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


# First bag of words, look if there is any correlation of some words and likes
def bag_of_words():
    # dataset = pd.DataFrame(id_of_post_to_data)
    dataset = pd.read_csv("../marry_items.csv")
    print(dataset)

    corpus = []
    for i in range(0, dataset.shape[0]):
        description_of_post = re.sub(u"ä", "ae", str(dataset["description_of_post"][i]))
        description_of_post = re.sub(u"ö", "oe", description_of_post)
        description_of_post = re.sub(u"ü", "ue", description_of_post)
        description_of_post = re.sub(u"ß", "ss", description_of_post)
        description_of_post = re.sub(
            "[^a-zA-Z]", " ", description_of_post
        )  # Remove punctuations ("." etc) with space.
        description_of_post = description_of_post.lower()  # All to lower case.
        description_of_post = (
            description_of_post.split()
        )  # Different element for different words

        porter_stemmer = PorterStemmer()
        all_stopwords = stopwords.words("german")
        # all_stopwords.remove("not")
        description_of_post = [
            porter_stemmer.stem(word)
            for word in description_of_post
            if word not in set(all_stopwords)
        ]
        description_of_post = " ".join(description_of_post)
        corpus.append(description_of_post)

    print(corpus)
    cv = CountVectorizer(max_features=1500)
    x = cv.fit_transform(corpus).toarray()
    from sklearn.impute import SimpleImputer

    imputer = SimpleImputer(missing_values=np.nan, strategy="mean")
    y = dataset["likes_of_post"].values.reshape(-1, 1)
    imputer.fit(y)
    y = imputer.transform(y)

    print(x.shape)
    print(y.shape)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.20, random_state=0
    )

    # =================================== Regression ================================
    from sklearn.linear_model import LinearRegression
    # from sklearn.ensemble import RandomForestRegressor

    # With multi linear regression we get Score:  -0.3073316723676951
    regressor = LinearRegression()
    # With random forest we get Score:  -9.612895334121241e-05
    # regressor = RandomForestRegressor(n_estimators=1000, random_state=0)
    regressor.fit(x_train, y_train)

    y_pred = regressor.predict(x_test)
    # TODO it is really bad, 1 is best and negative numbers mean it is REALLY bad
    np.set_printoptions(precision=2)
    print("Score: ", regressor.score(x_test, y_test))
    print("       Predicted      |     Actual     |      Difference")
    np.set_printoptions(
        suppress=True, formatter={"float_kind": "{:16.3f}".format}, linewidth=130
    )
    print(
        np.concatenate(
            (
                y_pred.reshape(len(y_pred), 1),
                y_test.reshape(len(y_test), 1),
                y_test - y_pred,
            ),
            axis=1,
        )
    )
    # print(y_test - y_pred)
    print("Correlation:")
    entries_count = len(cv.vocabulary_)
    words_used = np.array(list(cv.vocabulary_.keys()))
    correlation = np.concatenate(
        (words_used.reshape(entries_count, 1), regressor.coef_.reshape(entries_count, 1)),
        axis=1,
    )
    print(correlation)

    with open("prototype_correlation.csv", "w") as prototype_correlation_csv_file:
        fieldnames = ["word_used", "correlation"]
        writer = csv.DictWriter(prototype_correlation_csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for entry in correlation:
            writer.writerow({"word_used": entry[0], "correlation": entry[1]})


# Second Post Tager mit POS -> find out if post with eg nouns or adjectives have more likes
def post_tager(id_of_post_to_data):
    some_string = "Hello Stefan, i hope you had a really great day! I'm looking forward to see you at the house. " \
                  "It will cost 0.99 euro aka 1.25$ aka $1.25"
    tagged_text = nltk.pos_tag(nltk.Text(nltk.word_tokenize(some_string)))
    print(tagged_text)
    bar_dict = dict()
    for foo in tagged_text:
        if foo[1] in bar_dict:
            bar_dict[foo[1]] += 1
        else:
            bar_dict[foo[1]] = 1

    print(bar_dict)

    with open("prototype_tagged_stuff.csv", "w") as prototype_correlation_csv_file:
        fieldnames = ["id_of_post", "tagged_text"]
        writer = csv.DictWriter(prototype_correlation_csv_file, fieldnames=fieldnames)
        writer.writeheader()

        id_of_post_to_tagged_text = dict()
        for id_of_post, values in id_of_post_to_data.items():
            _, _, description_of_post = values

            tagged_text = nltk.pos_tag(nltk.Text(nltk.word_tokenize(some_string)))
            bar_dict = dict()
            for foo in tagged_text:
                if foo[1] in bar_dict:
                    bar_dict[foo[1]] += 1
                else:
                    bar_dict[foo[1]] = 1

            print(bar_dict)
            writer.writerow({"id_of_post": id_of_post, "tagged_text": bar_dict})



# Third Entity Recognition NER


if __name__ == '__main__':
    # bag_of_words()
    post_tager(id_of_post_to_data())


