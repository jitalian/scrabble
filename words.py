import string
import sys


class TrieNode:
    def __init__(self):
        self.children = {}
        self.complete_word = False


class Trie:
    def __init__(self, dict_file_path):
        self.root = TrieNode()
        self.dict_file_path = dict_file_path
        self.load_word_list()

    def insert_word(self, word):
        current_node = self.root
        for letter in word:
            if letter not in current_node.children:
                current_node.children[letter] = TrieNode()
            current_node = current_node.children[letter]
        current_node.complete_word = True

    def find_word(self, word):
        current_node = self.root
        for letter in word:
            # Will use lower case letters to signify a wild card letter and convert to upper during lookup
            if letter.upper() not in current_node.children:
                return False
            current_node = current_node.children[letter.upper()]
        return current_node.complete_word

    def load_word_list(self):
        with open(self.dict_file_path) as f:
            for line in f:
                word = line.strip()[1:-1].upper()
                self.insert_word(word)

    def find_prefix(self, prefix):
        current_node = self.root
        for letter in prefix:
            if letter.upper() not in current_node.children:
                return False
            current_node = current_node.children[letter.upper()]
        return True


# Testing code
def main():
    test_trie = Trie("word_list.txt")
    print(test_trie.find_word(('h', 'e', 'l', 'l', 'o')))
    print(test_trie.find_word("HELLOZ"))
    print(test_trie.find_prefix("ZYZ"))



if __name__ == "__main__":
    main()
