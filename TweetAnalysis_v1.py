import re


def split_hashtag(tag):
    """
    Splits hashtags into individual words

    :param tag: the hashtag
    """
    pattern = re.compile(r"[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
    return pattern.findall(tag)


def data_cleaning_2d(arr):
    """
    Removes double backslashes and hashtags and
    makes each word lowercase in a 2d array

    :param arr: the array to be cleaned
    :return: a new array without double backslashes
    """
    new_words = []
    for tweet in arr:
        for word in tweet:
            word = str(word).replace('\\', "")
            word = str(word).replace('-', "")
            if word.__contains__('#'):
                word = "{}".format(" ".join(split_hashtag(word)))
            word = word.lower()
            new_words.append(word)
    return new_words


def data_cleaning_1d(arr):
    """
    removes double backslashes and hashtags and
    makes all letters lower case in a 1d array

    :param arr: the array to be cleaned
    :return: a new array without double backslashes
    """
    new_words = []
    for word in arr:
        word = str(word).replace('\\', "")
        word = str(word).replace('#', "")
        if word.__contains__('#'):
            word = "{}".format(" ".join(split_hashtag(word)))
        word = word.lower()
        new_words.append(word)
    return new_words


def create_array(file_name):
    """
    creates a 2D array in which each element represents a word

    :param file_name: the name of the file
    :return: a 2D array holding each word in the file
    """
    with open(file_name, "r") as train_tweets:

        # determines the number of tweets in the file
        num_lines = 0
        content = train_tweets.read()
        lines = content.split("\n")

        for i in lines:
            num_lines += 1

        # creates a 1D array (each element represents a tweet)
        words = [0 for i in range(num_lines)]

        # creates a 2D array made up of 1D arrays (each element represents a word in the tweet)
        train_tweets.seek(0)
        for x in range(num_lines):
            tweet = train_tweets.readline()
            arr = tweet.split()
            words[x] = arr

        words = data_cleaning_2d(words)
        return words


def generate_true_score(file_name):
    """
    creates a dictionary with each word (key) and its associated score (value)

    :param file_name: the name of the file
    :return: a dictionary array holding each word and its score
    """
    arr = create_array(file_name)

    word_scores = {}
    for word in arr:
        # if word exists in the dictionary, update its score
        if word in word_scores:
            word_scores[word] += -1
        # if word doesn't exist in the dictionary, add it
        else:
            word_scores[word] = -1
    return word_scores


def generate_false_score(file_name):
    """
    creates a dictionary with each word (key) and its associated score (value)

    :param file_name: the name of the file
    :return: a dictionary array holding each word and its score
    """
    arr = create_array(file_name)

    word_scores = {}
    for word in arr:
        # if word exists in the dictionary, update its score
        if word in word_scores:
            word_scores[word] += 1
        # if word doesn't exist in the dictionary, add it
        else:
            word_scores[word] = 1
    return word_scores


def merge(dict1, dict2):
    """
    merges two dictionaries

    :param dict1: the first dictionary
    :param dict2: the second dictionary
    :return: the merged dictionary
    """
    dict3 = {**dict1, **dict2}
    return dict3


def print_score(dictionary):
    """
    prints a dictionary

    :param dictionary: the dictionary to be printed
    """
    for key, value in dictionary.items():
        print(key, ' : ', value)


def output_file(dictionary):
    """
    outputs the contents of a dictionary into a file

    :param dictionary: the dictionary
    """
    with open("word-scores.txt", "w") as word_scores:
        for key, value in dictionary.items():
            word_scores.write(key + " : " + str(value) + "\n")


def calculate_score(file_name, dictionary):
    """
    creates an array with the average sentiment score of each tweet

    :param file_name: the file with the tweets to be scored
    :param dictionary: the dictionary with the score of each word
    """
    with open(file_name, "r") as train_tweets:

        # determines the number of tweets in the file
        num_lines = 0
        content = train_tweets.read()
        lines = content.split("\n")

        for i in lines:
            num_lines += 1

        # creates a 1D array (each element represents the score of a tweet)
        scores = [0 for i in range(num_lines)]

    # converting the dictionary into a list
    key_list = list(dictionary.keys())

    # other variables
    total_score = 0
    max_score = 0
    i = 0
    num_words = 0

    for tweet in lines:
        tweet = data_cleaning_1d(tweet.split())
        for word in tweet:

            num_words += 1
            # the exact word exists in the dictionary
            if word in dictionary:
                total_score += dictionary[word]

            # a variation of the word exists in the dictionary
            else:
                for j in range(len(key_list)):
                    if key_list[j].__contains__(word):
                        # multiple keys in the dictionary may contain the word
                        # the key with the greatest (absolute) value will be included in total score
                        original_score = dictionary[key_list[j]]
                        absolute_score = abs(dictionary[key_list[j]])
                        max_score = max(max_score, absolute_score)

                        if max_score == absolute_score:
                            max_score = original_score

                total_score += max_score
                max_score = 0

        # average sentiment of tweet stored in an array
        scores[i] = round(total_score / num_words, 2)
        i += 1
        total_score = 0

    return scores


def main():

    true_score = generate_true_score("train-true.txt")
    false_score = generate_false_score("train-false.txt")
    total_score = merge(true_score, false_score)
    output_file(total_score)
    test_tweet_scores = calculate_score("test-short.txt", total_score)

    for score in test_tweet_scores:
        print(score)


if __name__ == "__main__":
    main()
