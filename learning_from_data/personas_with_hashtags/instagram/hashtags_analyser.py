import csv

HASHTAGS_FROM_PERSONAS = (
    "#local #cooking #bouldering #sports #lesssugar #traveling #healthy #grazblogger #happyme "
    "#backen #foodblogger #backenmachtglücklich #programming #memes #techlife #food #working "
    "#coffein #party #music #drinking #creativity #illustration #design #celebration #cooking "
    "#food #music #traveling #dog #dogslover #photography #art #family #familytime #friends "
    "#father #fatherandson #biking #family #mum #local #familienleben #decoration #handmade #nature"
).split(" ")


# CSV: HASHTAGS | # of users used it | is_already_in_any_persona
class hashtagsAnalyser:
    def analyse_hashtags(self):
        hashtags_to_number_of_uses = (
            self.hashtags_to_number_of_uses()
        )
        hashtags_to_data = self.hashtags_to_data(hashtags_to_number_of_uses)
        self.safe_data_in_csv(hashtags_to_data)

    @staticmethod
    def hashtags_to_number_of_uses():
        hashtags_to_number_of_uses = {}

        with open("persona_categorization.csv", newline="") as persona_categorization_csv_file:
            dict_reader = csv.DictReader(persona_categorization_csv_file)
            # Put CSV data in dict (ID: liked by)
            for row in dict_reader:
                hashtags = row["used_hashtags"].split()

                for hashtag in hashtags:
                    hashtag = "".join((filter(str.isalnum, hashtag)))
                    if "#" + hashtag in hashtags_to_number_of_uses.keys():
                        hashtags_to_number_of_uses["#" + hashtag] += 1
                    else:
                        hashtags_to_number_of_uses["#" + hashtag] = 1

        return hashtags_to_number_of_uses

    @staticmethod
    def hashtags_to_data(hashtags_to_number_of_uses):
        hashtags_to_data = dict()
        for hashtag, number_of_uses in hashtags_to_number_of_uses.items():
            if hashtag in HASHTAGS_FROM_PERSONAS:
                hashtags_to_data[hashtag] = (number_of_uses, "X")
            else:
                hashtags_to_data[hashtag] = (number_of_uses, "")

        return hashtags_to_data

    @staticmethod
    def safe_data_in_csv(hashtags_to_data):
        with open("used_hashtags.csv", "w", newline="") as used_hashtags_csv_file:
            fieldnames = ["hashtag", "number_of_users_who_used_it", "is_already_in_any_persona"]
            dict_writer = csv.DictWriter(
                used_hashtags_csv_file, fieldnames=fieldnames
            )

            dict_writer.writeheader()
            for (
                    hashtag,
                    data,
            ) in hashtags_to_data.items():
                number_of_users_who_used_it, is_already_in_any_persona = data
                dict_writer.writerow(
                    {
                        "hashtag": hashtag,
                        "number_of_users_who_used_it": number_of_users_who_used_it,
                        "is_already_in_any_persona": is_already_in_any_persona,
                    }
                )


if __name__ == "__main__":
    hashtags_analyser = hashtagsAnalyser()
    hashtags_analyser.analyse_hashtags()
