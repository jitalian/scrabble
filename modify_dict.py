
def fill_blanks(word):
    word_list = []
    for i in range(len(word)):
        word_list.append(word[:i] + "*" + word[i+1:])
    return word_list

def create_dict_with_blanks(filepath):

    with open(filepath, "w") as f:
        with open('word_list.txt') as w:
            for line in w:
                word = line.strip()[1:-1].upper()
                if len(word) > 15:
                    pass
                else:
                    f.write(word + '\n')

                if len(word) < 10:
                    for word_with_blank in fill_blanks(word):
                        f.write(word_with_blank + '\n')



create_dict_with_blanks("blanks_dict.txt")