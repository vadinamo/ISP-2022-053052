def get_n_grams(text, n):  # Получение словаря н-грам
    words = get_words(text)
    n_grams_dict = {}

    for word in words:
        if n <= len(word):
            for i in range(len(word)):
                count = 1
                if (i + n) <= len(word):
                    n_gram = word[i: (i + n)]

                    if n_gram in n_grams_dict.keys():
                        count = n_grams_dict[n_gram] + 1

                    n_grams_dict[n_gram] = count

    sorted_dict = {}
    sorted_keys = sorted(n_grams_dict, key=n_grams_dict.get, reverse=True)

    for w in sorted_keys:
        sorted_dict[w] = n_grams_dict[w]

    return sorted_dict


def get_words(text):  # Разбиение предложения на слова
    text = text.replace("\n", " ")
    text = text.replace(",", " ").replace(".", " ").replace("?", " ").replace("!", " ").replace(":", " ")
    text = text.replace('"', ' ').replace("'", "")
    text = text.lower()
    words = text.split()
    words.sort()
    return words


def number_of_words(words):  # Сколько раз встречается каждое слово
    words_dict = {}

    for i in range(len(words)):
        count = 1
        for j in range(len(words)):
            if i != j and words[i] == words[j]:
                count += 1

        words_dict[words[i]] = count

    return words_dict


def text_division(text):  # Разбиение текста на предложения
    text = text.replace("!", ".").replace("?", ".")
    sentences = text.split(".")
    sentences.pop()
    return sentences


def average_count(array):
    total_count = 0
    for i in array:
        total_count += i

    if len(array) == 0:
        length = 1
    else:
        length = len(array)

    return total_count / length


def median_count(array):
    array = sorted(array)
    if len(array) == 0:
        return 0
    elif len(array) % 2 == 1:
        return array[len(array) // 2]
    else:
        return (array[len(array) // 2 - 1] + array[len(array) // 2]) / 2


def data_input():
    k = 10
    n = 4

    print("Enter N")
    n_string = input("N=")
    try:
        n = int(n_string)
    except ValueError:
        print("'", n_string, "' is not int.\nN =", n)

    print("Enter K")
    k_string = input("K=")
    try:
        k = int(k_string)
    except ValueError:
        print("'", k_string, "' is not int.\nK =", k)

    print("Enter your string.")
    entered_string = input()

    return k, n, entered_string


def main():
    k, n, entered_string = data_input()

    sentences = {}
    for i in text_division(entered_string):
        sentences[i] = len(get_words(i))

    word_count = []
    for i in sentences.keys():
        word_count.append(sentences.get(i))

    print("Average number of words in a sentence:", int(average_count(word_count)))
    print("Median number of words in a sentence:", median_count(word_count))

    words_dict = number_of_words(get_words(entered_string))
    print("Words count:")
    if len(words_dict.keys()) == 0:
        print("None")
    else:
        for i in words_dict.keys():
            print(i, ":", words_dict.get(i))

    n_grams = get_n_grams(entered_string, n)
    count = 0
    
    print("Top %d %d-grams:" % (k, n))
    if len(n_grams.keys()) == 0 or k == 0:
        print("None")
    else:
        for key in n_grams.keys():
            if count < k:
                print(key, ":", n_grams[key])
                count += 1


if __name__ == '__main__':
    main()
