import random

from constants import SQUARES
from itertools import product
import string
import copy


class ComputerPlayer:
    def __init__(self, board, rack, dictionary, bag):
        self.board = board
        self.rack = rack
        self.bag = bag
        # self.rack.tiles = ['R', '*', 'W', 'B', 'R', 'T', 'O']
        # self.rack.tiles = ['R']
        self.dictionary = dictionary
        self.playable_board_locations = None
        self.allowed_tiles_horizontal_dict = None
        self.allowed_tiles_vertical_dict = None
        self.horizontal_score_lookup = [[{} for _ in range(SQUARES)] for _ in range(SQUARES)]
        self.vertical_score_lookup = [[{} for _ in range(SQUARES)] for _ in range(SQUARES)]
        self.blanks_values_dict_horizontal = {}
        self.blanks_values_dict_vertical = {}
        self.blank_chosen = "A"

    def get_active_tiles(self):

        self.playable_board_locations = set()
        for i in range(SQUARES):
            for j in range(SQUARES):
                if self.board.active_tiles[i][j] and self.board.current_board[i][j] == "_":
                    self.playable_board_locations.add((i, j))

    def check_allowed_vertical(self, row, col, tile):
        word = tile
        next_col = col + 1
        word_col = col

        word_multiplier = self.board.get_word_bonus(row, col, self.board.bonus_matrix)
        letter_multiplier = self.board.get_letter_bonus(row, col, self.board.bonus_matrix)

        letter_value = self.bag.get_tile_points(tile)
        score = letter_multiplier * letter_value

        while col > 0 and self.board.current_board[row][col - 1] != "_":
            word = (self.board.current_board[row][col - 1] + word)
            score += self.bag.get_tile_points(self.board.current_board[row][col - 1])
            col -= 1

        while next_col < SQUARES and self.board.current_board[row][next_col] != "_":
            word += self.board.current_board[row][next_col]
            score += self.bag.get_tile_points(self.board.current_board[row][next_col])
            next_col += 1

        if len(word) == 1:
            return True

        if self.dictionary.find_word(word.upper()):
            self.vertical_score_lookup[row][word_col][tile] = score * word_multiplier
            if tile == "*":
                self.blanks_values_dict_vertical[(row, word_col)] = set()
                for letter in string.ascii_lowercase:
                    if self.dictionary.find_word(word.replace("*", letter).upper()):
                        self.blanks_values_dict_vertical[(row, word_col)].add(letter)
            return True
        else:
            return False

    def check_allowed_horizontal(self, row, col, tile):
        word = tile
        next_row = row + 1
        word_row = row

        word_multiplier = self.board.get_word_bonus(row, col, self.board.bonus_matrix)
        letter_multiplier = self.board.get_letter_bonus(row, col, self.board.bonus_matrix)

        letter_value = self.bag.get_tile_points(tile)
        score = letter_multiplier * letter_value

        while row > 0 and self.board.current_board[row - 1][col] != "_":
            word = (self.board.current_board[row - 1][col] + word)
            score += self.bag.get_tile_points(self.board.current_board[row - 1][col])
            row -= 1

        while next_row < SQUARES and self.board.current_board[next_row][col] != "_":
            word += self.board.current_board[next_row][col]
            score += self.bag.get_tile_points(self.board.current_board[next_row][col])
            next_row += 1

        if len(word) == 1:
            return True

        if self.dictionary.find_word(word.upper()):
            self.horizontal_score_lookup[word_row][col][tile] = score * word_multiplier
            if tile == "*":
                self.blanks_values_dict_horizontal[(word_row, col)] = set()
                for letter in string.ascii_lowercase:
                    if self.dictionary.find_word(word.replace("*", letter).upper()):
                        self.blanks_values_dict_horizontal[(word_row, col)].add(letter)
            return True
        else:
            return False

    def get_allowed_tiles(self):

        self.allowed_tiles_horizontal_dict = {location: set(self.rack.tiles) for location in self.playable_board_locations}
        self.allowed_tiles_vertical_dict = {location: set(self.rack.tiles) for location in self.playable_board_locations}
        for location in self.playable_board_locations:
            for tile in set(self.rack.tiles):
                if not self.check_allowed_vertical(location[0], location[1], tile):
                    self.allowed_tiles_vertical_dict[location].remove(tile)
                if not self.check_allowed_horizontal(location[0], location[1], tile):
                    self.allowed_tiles_horizontal_dict[location].remove(tile)

    def word_from_rack_horizontal(self, word, row, col, rack_dict):

        rack_dict_copy = copy.copy(rack_dict)
        for letter in word:
            if self.board.current_board[row][col].upper() == letter:
                col += 1
                continue
            else:
                rack_dict_copy[letter] -= 1
                if rack_dict_copy[letter] == -1:
                    return False
                col += 1
        return True

    def word_from_rack_vertical(self, word, row, col, rack_dict):

        rack_dict_copy = copy.copy(rack_dict)
        for letter in word:
            if self.board.current_board[row][col].upper() == letter:
                row += 1
                continue
            else:
                rack_dict_copy[letter] -= 1
                if rack_dict_copy[letter] == -1:
                    return False
                row += 1
        return True

    def get_set_lookup_matrix(self, horizontal):
        set_lookup_matrix = []
        for i in range(SQUARES):
            row = []
            for j in range(SQUARES):
                if self.board.current_board[i][j] != "_":
                    row.append({self.board.current_board[i][j].upper()})
                elif (i, j) in self.playable_board_locations:
                    if horizontal:
                        row.append(self.allowed_tiles_horizontal_dict[(i, j)])
                    else:
                        row.append(self.allowed_tiles_vertical_dict[(i, j)])
                else:
                    row.append(set(self.rack.tiles))
            set_lookup_matrix.append(row)

        return set_lookup_matrix

    def get_word_lane_horizontal(self, row, col, lane_length, set_lookup_matrix):
        word_lane = []
        tiles_placed = 0
        valid_lane = 0
        start_col = col

        if (row, col) in self.playable_board_locations or self.board.current_board[row][col] != "_":
            if start_col != 0 and self.board.current_board[row][start_col - 1] != "_":
                while start_col > 0 and self.board.current_board[row][start_col - 1] != "_":
                    word_lane.insert(0, {self.board.current_board[row][start_col - 1].upper()})
                    start_col -= 1

        while tiles_placed < lane_length and col < SQUARES:
            if (row, col) in self.playable_board_locations:
                valid_lane = 1

            if self.board.current_board[row][col] != "_":
                word_lane.append({self.board.current_board[row][col].upper()})
                col += 1
            else:
                word_lane.append(set_lookup_matrix[row][col])
                col += 1
                tiles_placed += 1

                if tiles_placed == lane_length and col != SQUARES:
                    while col < SQUARES and self.board.current_board[row][col] != "_":
                        word_lane.append({self.board.current_board[row][col].upper()})
                        col += 1

        if tiles_placed != lane_length or set() in word_lane or len(word_lane) > 9:
            return False, start_col

        if valid_lane:
            return word_lane, start_col

        return False, start_col

    def get_word_lane_vertical(self, row, col, lane_length, set_lookup_matrix):
        word_lane = []
        tiles_placed = 0
        valid_lane = 0
        start_row = row

        if (row, col) in self.playable_board_locations or self.board.current_board[row][col] != "_":
            if start_row != 0 and self.board.current_board[start_row - 1][col] != "_":
                while start_row > 0 and self.board.current_board[start_row - 1][col] != "_":
                    word_lane.insert(0, {self.board.current_board[start_row - 1][col].upper()})
                    start_row -= 1

        while tiles_placed < lane_length and row < SQUARES:
            if (row, col) in self.playable_board_locations:
                valid_lane = 1

            if self.board.current_board[row][col] != "_":
                word_lane.append({self.board.current_board[row][col].upper()})
                row += 1
            else:
                word_lane.append(set_lookup_matrix[row][col])
                row += 1
                tiles_placed += 1

                if tiles_placed == lane_length and row != SQUARES:
                    while row < SQUARES and self.board.current_board[row][col] != "_":
                        word_lane.append({self.board.current_board[row][col].upper()})
                        row += 1

        if tiles_placed != lane_length or set() in word_lane or len(word_lane) > 9:
            return False, start_row

        if valid_lane:
            return word_lane, start_row

        return False, start_row

    def calculate_word_score_horizontal(self, location, word):

        main_word_score = 0
        sub_word_scores = []
        multiplier = 1
        blank_value = None
        tiles_placed = 0

        row, col = location[0], location[1]

        for letter in word:

            if self.board.current_board[row][col].upper() == letter:
                main_word_score += self.bag.get_tile_points(letter)
                col += 1

            elif letter == "*" and (row, col) in self.blanks_values_dict_horizontal:
                blank_value = None
                for blank_letter in self.blanks_values_dict_horizontal[(row, col)]:
                    if self.dictionary.find_word(word.replace("*", blank_letter.upper())):
                        blank_value = blank_letter
                        break

                if blank_value is None:
                    return word, False, blank_value

                word = word.replace("*", blank_value)
                col += 1
                tiles_placed += 1

            else:
                multiplier *= self.board.get_word_bonus(row, col, self.board.bonus_matrix)

                if letter in self.horizontal_score_lookup[row][col]:
                    sub_word_scores.append(self.horizontal_score_lookup[row][col][letter])

                letter_multiplier = self.board.get_letter_bonus(row, col, self.board.bonus_matrix)

                letter_score = self.bag.get_tile_points(letter)
                main_word_score += (letter_score * letter_multiplier)

                col += 1
                tiles_placed += 1

        main_word_score *= multiplier
        move_score = main_word_score
        for score in sub_word_scores:
            move_score += score

        if tiles_placed == 7:
            move_score += 50

        return word, move_score, blank_value

    def calculate_word_score_vertical(self, location, word):
        main_word_score = 0
        sub_word_scores = []
        multiplier = 1
        blank_value = None
        tiles_placed = 0

        row, col = location[0], location[1]

        for letter in word:

            if self.board.current_board[row][col].upper() == letter:
                main_word_score += self.bag.get_tile_points(letter)
                row += 1

            elif letter == "*" and (row, col) in self.blanks_values_dict_vertical:
                blank_value = None
                for blank_letter in self.blanks_values_dict_vertical[(row, col)]:
                    if self.dictionary.find_word(word.replace("*", blank_letter.upper())):
                        blank_value = blank_letter
                        break

                if blank_value is None:
                    return word, False, blank_value

                word = word.replace("*", blank_value)
                row += 1
                tiles_placed += 1

            else:
                multiplier *= self.board.get_word_bonus(row, col, self.board.bonus_matrix)

                if letter in self.vertical_score_lookup[row][col]:
                    sub_word_scores.append(self.vertical_score_lookup[row][col][letter])

                letter_multiplier = self.board.get_letter_bonus(row, col, self.board.bonus_matrix)

                letter_score = self.bag.get_tile_points(letter)
                main_word_score += (letter_score * letter_multiplier)

                row += 1
                tiles_placed += 1

        main_word_score *= multiplier
        move_score = main_word_score
        for score in sub_word_scores:
            move_score += score

        if tiles_placed == 7:
            move_score += 50

        return word, move_score, blank_value

    def play_best_move_horizontal(self, best_move):

        self.board.cpu_score += best_move[2]

        row, col = best_move[0][0], best_move[0][1]
        tiles_to_replace = 0

        for letter in best_move[1]:
            if self.board.current_board[row][col].upper() == letter:
                col += 1
            elif self.board.current_board[row][col] == "_" and letter != "*" and not letter.islower():
                self.board.current_board[row][col] = letter
                self.board.update_active_tiles(row, col)
                self.rack.tiles.remove(letter)
                tiles_to_replace += 1
                col += 1
            else:
                self.rack.tiles.remove("*")
                if letter != "*":
                    self.board.current_board[row][col] = letter
                    self.board.update_active_tiles(row, col)
                    tiles_to_replace += 1
                    col += 1
                else:
                    for blank_letter in string.ascii_lowercase:
                        letter_found = False
                        if self.dictionary.find_word(best_move[1].replace("*", blank_letter).upper()):
                            self.board.current_board[row][col] = blank_letter
                            self.blank_chosen = blank_letter
                            self.board.update_active_tiles(row, col)
                            tiles_to_replace += 1
                            letter_found = True
                            col += 1

                        if letter_found:
                            break

        for i in range(tiles_to_replace):
            if "*" in self.rack.tiles:
                new_tile = self.bag.get_random_tile(False)
            else:
                new_tile = self.bag.get_random_tile()

            if new_tile is not None:
                self.rack.tiles.append(new_tile)

    def play_best_move_vertical(self, best_move):
        self.board.cpu_score += best_move[2]

        row, col = best_move[0][0], best_move[0][1]
        tiles_to_replace = 0

        for letter in best_move[1]:
            if self.board.current_board[row][col].upper() == letter:
                row += 1
            elif self.board.current_board[row][col] == "_" and letter != "*" and not letter.islower():
                self.board.current_board[row][col] = letter
                self.board.update_active_tiles(row, col)
                self.rack.tiles.remove(letter)
                tiles_to_replace += 1
                row += 1
            else:
                self.rack.tiles.remove("*")
                if letter != "*":
                    self.board.current_board[row][col] = letter
                    self.board.update_active_tiles(row, col)
                    tiles_to_replace += 1
                    row += 1
                else:
                    for blank_letter in string.ascii_lowercase:
                        letter_found = False
                        if self.dictionary.find_word(best_move[1].replace("*", blank_letter).upper()):
                            self.board.current_board[row][col] = blank_letter
                            self.blank_chosen = blank_letter
                            self.board.update_active_tiles(row, col)
                            tiles_to_replace += 1
                            letter_found = True
                            row += 1

                        if letter_found:
                            break

        for i in range(tiles_to_replace):
            if "*" in self.rack.tiles:
                new_tile = self.bag.get_random_tile(False)
            else:
                new_tile = self.bag.get_random_tile()

            if new_tile is not None:
                self.rack.tiles.append(new_tile)

    def get_one_letter_move(self, row, col, tile, horizontal_matrix, vertical_matrix):
        possible_letters = horizontal_matrix[row][col].intersection(vertical_matrix[row][col])
        if len(possible_letters) == 0:
            return False
        else:
            score = 0
            horizontal = False
            vertical = False

            if tile not in possible_letters:
                return False

            if tile in self.horizontal_score_lookup[row][col]:
                score += self.horizontal_score_lookup[row][col][tile]
                horizontal = True
                # print("HORIZONTAL BLANKS", (row, col), self.blanks_values_dict_horizontal[(row, col)])

            if tile in self.vertical_score_lookup[row][col]:
                score += self.vertical_score_lookup[row][col][tile]
                vertical = True
                # print("VERTICAL BLANKS", (row, col), self.blanks_values_dict_vertical[(row, col)])

            if score > 0:
                if tile == "*":
                    if horizontal and not vertical:
                        tile = random.choice(list(self.blanks_values_dict_horizontal[(row, col)]))
                    if vertical and not horizontal:
                        tile = random.choice(list(self.blanks_values_dict_vertical[(row, col)]))
                    if vertical and horizontal:
                        blanks_set = self.blanks_values_dict_horizontal[(row, col)].intersection(self.blanks_values_dict_vertical[(row, col)])
                        if len(blanks_set) == 0:
                            return False
                        else:
                            tile = random.choice(list(blanks_set))
                return [(row, col), tile, score]
            else:
                return False

    def play_one_letter(self, move):

        self.board.cpu_score += move[2]
        self.board.current_board[move[0][0]][move[0][1]] = move[1]

    def cpu_move(self):
        best_move_horizontal = [0, 0, 0]  # [location, word, score]
        best_move_vertical = [0, 0, 0]  # [location, word, score]
        best_move_one_tile = [0, 0, 0]

        rack_counts_dict = {tile: self.rack.tiles.count(tile) for tile in self.rack.tiles}
        self.get_active_tiles()
        self.get_allowed_tiles()
        matrix_horizontal = self.get_set_lookup_matrix(True)
        matrix_vertical = self.get_set_lookup_matrix(False)
        word_set_horizontal = set()
        word_set_vertical = set()

        # print("HORIZONTAL")
        # for row in self.horizontal_score_lookup:
        #     print(row)
        # for row in matrix_horizontal:
        #     print(row)
        # print("VERTICAL")
        # for row in self.vertical_score_lookup:
        #     print(row)
        # for row in matrix_vertical:
        #     print(row)

        # print(self.blanks_values_dict_vertical)
        # print(self.blanks_values_dict_horizontal)

        for row in range(SQUARES):
            for col in range(SQUARES):
                for tile in self.rack.tiles:
                    if self.board.current_board[row][col] == "_":
                        move = self.get_one_letter_move(row, col, tile, matrix_horizontal, matrix_vertical)
                        if move is not False:
                            if move[2] > best_move_one_tile[2]:
                                best_move_one_tile = move
                for i in range(2, len(self.rack.tiles) + 1, 1):
                    lane_horizontal, start_col = self.get_word_lane_horizontal(row, col, i, matrix_horizontal)
                    lane_vertical, start_row = self.get_word_lane_vertical(row, col, i, matrix_vertical)
                    if lane_horizontal is not False:
                        word_set_horizontal = word_set_horizontal.union(self.find_words(lane_horizontal, rack_counts_dict, row, start_col, True))
                    if lane_vertical is not False:
                        word_set_vertical = word_set_vertical.union(self.find_words(lane_vertical, rack_counts_dict, start_row, col, False))

        for location, word in word_set_horizontal:
            word, score, blank_value = self.calculate_word_score_horizontal(location, word)
            if score is not False:
                if score > best_move_horizontal[2]:
                    best_move_horizontal = [location, word, score]

        for location, word in word_set_vertical:
            word, score, blank_value = self.calculate_word_score_vertical(location, word)
            if score is not False:
                if score > best_move_vertical[2]:
                    best_move_vertical = [location, word, score]

        print("BEST MOVE VERTICAL: ", best_move_vertical)
        print("BEST MOVE HORIZONTAL: ", best_move_horizontal)
        print("BEST MOVE ONE TILE: ", best_move_one_tile)
        if len(word_set_vertical) == 0 and len(word_set_horizontal) == 0 and best_move_one_tile == [0, 0, 0]:
            return False

        print(self.board.current_board)
        print("RACK BEFORE: ", self.rack.tiles)

        if best_move_vertical[2] > best_move_horizontal[2] and best_move_vertical[2] > best_move_one_tile[2]:
            self.play_best_move_vertical(best_move_vertical)
            print("RACK AFTER: ", self.rack.tiles)
            word = str(best_move_vertical[1]).lower().replace("*", self.blank_chosen)
            self.board.cpu_last_move_text = f"CPU: {word} for {best_move_vertical[2]}!"
            return best_move_vertical

        elif best_move_horizontal[2] > best_move_one_tile[2]:
            self.play_best_move_horizontal(best_move_horizontal)
            print("RACK AFTER: ", self.rack.tiles)
            word = str(best_move_horizontal[1]).lower().replace("*", self.blank_chosen)
            self.board.cpu_last_move_text = f"CPU: {word} for {best_move_horizontal[2]}!"
            return best_move_horizontal
        else:
            self.play_one_letter(best_move_one_tile)

            self.board.cpu_last_move_text = f"CPU: Letter {str(best_move_one_tile[1]).lower()} for {best_move_one_tile[2]}!"
            print("RACK AFTER: ", self.rack.tiles)
            return best_move_one_tile

    def find_words(self, letter_sets, rack_dict, row, col, horizontal):

        if len(letter_sets) == 2:
            words_set = set()
            for i in product(letter_sets[0], letter_sets[1]):
                word = ''.join(i)
                if horizontal:
                    if self.dictionary.find_word(word) and self.word_from_rack_horizontal(word, row, col, rack_dict):
                        words_set.add(((row, col), word))
                else:
                    if self.dictionary.find_word(word) and self.word_from_rack_vertical(word, row, col, rack_dict):
                        words_set.add(((row, col), word))
            return words_set
        else:
            prefix_set = set()
            for i in product(letter_sets[0], letter_sets[1]):
                prefix = ''.join(i)
                if horizontal:
                    if self.dictionary.find_prefix(prefix) and self.word_from_rack_horizontal(prefix, row, col, rack_dict):
                        prefix_set.add(prefix)
                else:
                    if self.dictionary.find_prefix(prefix) and self.word_from_rack_vertical(prefix, row, col, rack_dict):
                        prefix_set.add(prefix)
            return self.find_words([prefix_set, *letter_sets[2:]], rack_dict, row, col, horizontal)
