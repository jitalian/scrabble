from constants import SQUARES
from itertools import product
import string
import copy


class ComputerPlayer:
    def __init__(self, board, rack, dictionary):
        self.board = board
        self.rack = rack
        self.dictionary = dictionary
        self.playable_board_locations = None
        self.allowed_tiles_horizontal_dict = None
        self.allowed_tiles_vertical_dict = None
        self.best_move = []

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

        # TODO add check for single tile placed here and in vertical function
        if self.dictionary.find_word(word):
            return True
        else:
            return False

    def get_allowed_tiles(self):

        if "*" in self.rack.tiles:
            self.allowed_tiles_horizontal_dict = {location: set(string.ascii_lowercase) for location in self.playable_board_locations}
            self.allowed_tiles_vertical_dict = {location: set(string.ascii_lowercase) for location in self.playable_board_locations}
            for location in self.playable_board_locations:
                for tile in set(string.ascii_lowercase):
                    if not self.check_allowed_vertical(location[0], location[1], tile):
                        self.allowed_tiles_vertical_dict[location].remove(tile)
                    if not self.check_allowed_horizontal(location[0], location[1], tile):
                        self.allowed_tiles_horizontal_dict[location].remove(tile)

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
                if letter in rack_dict_copy:
                    rack_dict_copy[letter] -= 1
                    if rack_dict_copy[letter] == -1:
                        return False
                elif "*" in rack_dict_copy:
                    rack_dict_copy["*"] -= 1
                    if rack_dict_copy["*"] == -1:
                        return False
                col += 1

        return True

    def get_moves_one_location_horizontal(self, location, size, rack_counts_dict):

        rack_set = set(self.rack.tiles)
        move_lane_left = []
        move_lane_right = []
        row, col = location[0], location[1]
        start_col = col
        end_col = col
        lane_length = 1
        while start_col > 0 and lane_length < size:
            if self.board.current_board[row][start_col] != "_":
                start_col -= 1
            else:
                start_col -= 1
                lane_length += 1

        current_col = start_col
        while current_col <= col:
            if (row, current_col) in self.playable_board_locations:
                move_lane_left.append(self.allowed_tiles_horizontal_dict[(row, current_col)])
                current_col += 1
            elif self.board.current_board[row][current_col] != "_":
                move_lane_left.append(self.board.current_board[row][current_col])
                current_col += 1
            else:
                move_lane_left.append(rack_set)
                current_col += 1

        # print("Left", location, move_lane_left)
        words_list_left = []
        for i in product(*move_lane_left):
            if self.dictionary.find_word(''.join(i)):
                if self.word_from_rack(i, row, start_col, rack_counts_dict):
                    words_list_left.append(''.join(i))
        print("LEFT", location, words_list_left)

        lane_length = 1
        while end_col < SQUARES - 1 and lane_length < size:
            if self.board.current_board[row][end_col] != "_":
                end_col += 1
            else:
                end_col += 1
                lane_length += 1

        current_col = col
        while current_col <= end_col:
            if (row, current_col) in self.playable_board_locations:
                move_lane_right.append(self.allowed_tiles_horizontal_dict[(row, current_col)])
                current_col += 1
            elif self.board.current_board[row][current_col] != "_":
                move_lane_right.append(self.board.current_board[row][current_col])
                current_col += 1
            else:
                move_lane_right.append(rack_set)
                current_col += 1

        words_list_right = []
        for i in product(*move_lane_right):
            if self.dictionary.find_word(''.join(i)):
                if self.word_from_rack(i, row, col, rack_counts_dict):
                    words_list_right.append(''.join(i))

        # print("Right", location, move_lane_right)
        print("RIGHT", location, words_list_right)

    def cpu_move(self):
        print(self.rack.tiles)
        rack_counts_dict = {tile: self.rack.tiles.count(tile) for tile in self.rack.tiles}
        self.get_active_tiles()
        self.get_allowed_tiles()
        for location in self.playable_board_locations:
            for size in range(2, 8, 1):
                self.get_moves_one_location_horizontal(location, size, rack_counts_dict)

        # for row in self.board.active_tiles:
        #     print(row)
