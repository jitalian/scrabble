from constants import SQUARES
from itertools import product
import string
import copy


class ComputerPlayer:
    def __init__(self, board, rack, dictionary):
        self.board = board
        self.rack = rack
        self.rack.tiles = ['A', '*', 'C', 'T', 'I', 'E', 'E']
        self.dictionary = dictionary
        self.playable_board_locations = None
        self.allowed_tiles_horizontal_dict = None
        self.allowed_tiles_vertical_dict = None
        self.best_move = ["", (0, 0), "", 0]
        horizontal_score_lookup = [[0 for _ in range(SQUARES)] for _ in range(SQUARES)]

    def get_active_tiles(self):

        self.playable_board_locations = set()
        for i in range(SQUARES):
            for j in range(SQUARES):
                if self.board.active_tiles[i][j] and self.board.current_board[i][j] == "_":
                    self.playable_board_locations.add((i, j))

    def check_allowed_vertical(self, row, col, tile):
        word = tile
        next_col = col + 1
        if tile == "*":
            return True

        while col > 0 and self.board.current_board[row][col - 1] != "_":
            word = (self.board.current_board[row][col - 1] + word)
            col -= 1

        while next_col < SQUARES and self.board.current_board[row][next_col] != "_":
            word += self.board.current_board[row][next_col]
            next_col += 1

        if len(word) == 1:
            return True

        if self.dictionary.find_word(word):
            return True
        else:
            return False

    def check_allowed_horizontal(self, row, col, tile):
        word = tile
        next_row = row + 1
        if tile == "*":
            return True

        while row > 0 and self.board.current_board[row - 1][col] != "_":
            word = (self.board.current_board[row - 1][col] + word)
            row -= 1

        while next_row < SQUARES and self.board.current_board[next_row][col] != "_":
            word += self.board.current_board[next_row][col]
            next_row += 1

        if len(word) == 1:
            return True

        if self.dictionary.find_word(word):
            return True
        else:
            return False

    def get_allowed_tiles(self):

        if "*" in self.rack.tiles:
            self.allowed_tiles_horizontal_dict = {location: set(string.ascii_lowercase).union(set(self.rack.tiles)) for location in self.playable_board_locations}
            self.allowed_tiles_vertical_dict = {location: set(string.ascii_lowercase).union(set(self.rack.tiles)) for location in self.playable_board_locations}
            for location in self.playable_board_locations:
                for tile in set(string.ascii_lowercase):
                    if not self.check_allowed_vertical(location[0], location[1], tile):
                        self.allowed_tiles_vertical_dict[location].remove(tile)
                        if tile.upper in set(self.rack.tiles):
                            self.allowed_tiles_vertical_dict[location].remove(tile.upper())
                    if not self.check_allowed_horizontal(location[0], location[1], tile):
                        self.allowed_tiles_horizontal_dict[location].remove(tile)
                        if tile.upper in set(self.rack.tiles):
                            self.allowed_tiles_horizontal_dict[location].remove(tile.upper())

        else:
            self.allowed_tiles_horizontal_dict = {location: set(self.rack.tiles) for location in self.playable_board_locations}
            self.allowed_tiles_vertical_dict = {location: set(self.rack.tiles) for location in self.playable_board_locations}
            for location in self.playable_board_locations:
                for tile in set(self.rack.tiles):
                    if not self.check_allowed_vertical(location[0], location[1], tile):
                        self.allowed_tiles_vertical_dict[location].remove(tile)
                    if not self.check_allowed_horizontal(location[0], location[1], tile):
                        self.allowed_tiles_horizontal_dict[location].remove(tile)

    def word_from_rack(self, word, row, col, rack_dict):

        rack_dict_copy = copy.copy(rack_dict)
        for letter in word:
            if self.board.current_board[row][col] == letter:
                col += 1
                continue
            else:
                if letter.isupper():
                    rack_dict_copy[letter] -= 1
                    if rack_dict_copy[letter] == -1:
                        return False
                elif letter.islower():
                    rack_dict_copy["*"] -= 1
                    if rack_dict_copy["*"] == -1:
                        return False
                col += 1

        return True

    # @staticmethod
    # def prefix_from_rack(prefix, rack_dict, row, col):
    #     rack_dict_copy = copy.copy(rack_dict)
    #     for letter in prefix:
    #         if letter.islower():
    #             rack_dict_copy["*"] -= 1
    #             if rack_dict_copy["*"] == -1:
    #                 return False
    #         else:
    #             rack_dict_copy[letter] -= 1
    #             if rack_dict_copy[letter] == -1:
    #                 return False
    #     return True

    def get_set_lookup_matrix(self):
        contains_wild_card = "*" in self.rack.tiles
        set_lookup_matrix = []
        for i in range(SQUARES):
            row = []
            for j in range(SQUARES):
                if self.board.current_board[i][j] != "_":

                    row.append({self.board.current_board[i][j]})
                elif (i, j) in self.playable_board_locations:
                    row.append(self.allowed_tiles_horizontal_dict[(i, j)])
                else:
                    if contains_wild_card:
                        row.append(set(string.ascii_lowercase).union(set(self.rack.tiles)))
                    else:
                        row.append(set(self.rack.tiles))
            set_lookup_matrix.append(row)

        return set_lookup_matrix

    def get_word_lane(self, row, col, lane_length, set_lookup_matrix):
        word_lane = []
        tiles_placed = 0
        valid_lane = 0
        start_col = col

        if (row, col) in self.playable_board_locations or self.board.current_board[row][col] != "_":
            if start_col != 0 and self.board.current_board[row][start_col - 1] != "_":
                while start_col > 0 and self.board.current_board[row][start_col - 1] != "_":
                    word_lane.insert(0, {self.board.current_board[row][start_col - 1]})
                    start_col -= 1

        while tiles_placed < lane_length and col < SQUARES:
            if (row, col) in self.playable_board_locations:
                valid_lane = 1

            if self.board.current_board[row][col] != "_":
                word_lane.append({self.board.current_board[row][col]})
                col += 1
            else:
                word_lane.append(set_lookup_matrix[row][col])
                col += 1
                tiles_placed += 1

                if tiles_placed == lane_length and col - 1 != SQUARES - 1:
                    while self.board.current_board[row][col] != "_":
                        word_lane.append({self.board.current_board[row][col]})
                        col += 1

        if tiles_placed != lane_length or set() in word_lane:
            return False, start_col

        if valid_lane:
            return word_lane, start_col

        return False, start_col

    def get_score(self, word, location):
        pass

    def cpu_move(self):
        rack_counts_dict = {tile: self.rack.tiles.count(tile) for tile in self.rack.tiles}
        self.get_active_tiles()
        self.get_allowed_tiles()
        matrix = self.get_set_lookup_matrix()
        word_set = set()
        for row in range(SQUARES):
            for col in range(SQUARES):
                for i in range(2, len(self.rack.tiles) + 1, 1):
                    lane, start_col = self.get_word_lane(row, col, i, matrix)
                    if lane is not False:
                        self.find_words(lane, rack_counts_dict, row, start_col)


        print("HERE")
        # self.find_words([set(string.ascii_lowercase).union(set(self.rack.tiles)) for i in range(7)], rack_counts_dict)

        # print(count)
        # self.get_word_lane(7, 1, 7, matrix)
        # for location in self.playable_board_locations:
        #     for size in range(2, 8, 1):
        #         self.get_moves_one_location_horizontal(location, size, rack_counts_dict)
        # print("HERE")
        # for row in self.board.active_tiles:
        #     print(row)

    def find_words(self, letter_sets, rack_dict, row, col):

        if len(letter_sets) == 2:
            words_set = set()
            for i in product(letter_sets[0], letter_sets[1]):
                word = ''.join(i)
                if self.dictionary.find_word(word) and self.word_from_rack(word, row, col, rack_dict):
                    words_set.add(word)
            return words_set
        else:
            prefix_set = set()
            for i in product(letter_sets[0], letter_sets[1]):
                prefix = ''.join(i)
                if self.dictionary.find_prefix(prefix) and self.word_from_rack(prefix, row, col, rack_dict):
                    prefix_set.add(prefix)
            return self.find_words([prefix_set, *letter_sets[2:]], rack_dict, row, col)



