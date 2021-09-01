class LevenshteinDistanceCalculator:
    @staticmethod
    def levenshtein_distance_of_words(first_word, second_word):
        length_of_first_word = len(first_word)
        length_of_second_word = len(second_word)
        sub_problem_matrix = [
            [0] * (length_of_second_word + 1) for _ in range(length_of_first_word + 1)
        ]

        for first_word_index in range(length_of_first_word + 1):
            sub_problem_matrix[first_word_index][0] = first_word_index
        for second_word_index in range(length_of_second_word + 1):
            sub_problem_matrix[0][second_word_index] = second_word_index

        for first_word_index in range(1, length_of_first_word + 1):
            for second_word_index in range(1, length_of_second_word + 1):
                if (
                    first_word[first_word_index - 1]
                    == second_word[second_word_index - 1]
                ):
                    sub_problem_matrix[first_word_index][
                        second_word_index
                    ] = sub_problem_matrix[first_word_index - 1][second_word_index - 1]
                else:
                    sub_problem_matrix[first_word_index][second_word_index] = 1 + min(
                        sub_problem_matrix[first_word_index - 1][second_word_index],
                        sub_problem_matrix[first_word_index][second_word_index - 1],
                        sub_problem_matrix[first_word_index - 1][second_word_index - 1],
                    )

        return sub_problem_matrix[-1][-1]

    def levenshtein_distances_matrix(self, list_of_words):
        number_of_words = len(list_of_words)
        levenshtein_distances_matrix = [
            [0] * (number_of_words) for _ in range(number_of_words)
        ]

        for index_first_word in range(number_of_words):
            for index_second_word in range(number_of_words):
                levenshtein_distances_matrix[index_first_word][index_second_word] = self.levenshtein_distance_of_words(list_of_words[index_first_word], list_of_words[index_second_word])
        self.print_levenshtein_matrix(list_of_words, levenshtein_distances_matrix)

    @staticmethod
    def print_levenshtein_matrix(list_of_words, levenshtein_distances_matrix):
        print(list_of_words)
        for distances_of_words in levenshtein_distances_matrix:
            print(distances_of_words)


if __name__ == "__main__":
    levenshtein_distance_calculator = LevenshteinDistanceCalculator()
    levenshtein_distance_of_words = (
        levenshtein_distance_calculator.levenshtein_distance_of_words("Zelda", "Link")
    )
    print("levenshtein_distance_of_words: ", levenshtein_distance_of_words)
    print("\n\n ================= \n\n")
    list_of_words = ["Zelda", "Link", "Foo", "Bar", "Risk", "Think"]
    levenshtein_distances_matrix = (
        levenshtein_distance_calculator.levenshtein_distances_matrix(list_of_words)
    )
