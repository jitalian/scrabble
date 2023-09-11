def fill_blanks(word):
    """Returns a list of words where 1 letter of the given word is replaced with a blank "*" value"""

    word_list = []
    for i in range(len(word)):
        word_list.append(word[:i] + "*" + word[i + 1:])
    return word_list


def create_dict_with_blanks(filepath):
    words_set = set()

    with open('word_list.txt') as w:
        for line in w:
            word = line.strip()[1:-1].upper()
            if len(word) > 15:
                pass
            else:
                words_set.add(word)

            # Limit the number of blanks for very long words to save space
            if len(word) < 10:
                for word_with_blank in fill_blanks(word):
                    words_set.add(word_with_blank)

        print(len(words_set))

    with open(filepath, "w") as f:
        for word in words_set:
            f.write(word + '\n')


create_dict_with_blanks("blanks_dict.txt")
