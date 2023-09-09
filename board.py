from constants import BOARD_WIDTH, WINDOW_WIDTH, SQUARES, PADDING, FONT_SIZE, COLORS
import pygame
from rack import Rack
import numpy
import string


class GameBoard:
    def __init__(self, screen, bag, dictionary):

        self.dictionary = dictionary
        self.first_move = True
        self.bag = bag
        self.screen = screen
        self.triple_word_squares = {(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)}
        self.triple_letter_squares = {(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5),
                                      (9, 9), (9, 13), (13, 5), (13, 9)}
        self.double_letter_squares = {(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2),
                                      (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8),
                                      (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)}
        self.double_word_squares = {(1, 1), (1, 13), (2, 2), (2, 12), (3, 3), (3, 11), (4, 4), (4, 10),
                                    (10, 4), (10, 10), (11, 3), (11, 11), (12, 2), (12, 12), (13, 1), (13, 13)}
        self.start = (7, 7)

        self.bonus_matrix = [[("_", "_") for _ in range(SQUARES)] for _ in range(SQUARES)]
        self.generate_bonus_matrix()

        self.active_tiles = [[False for _ in range(SQUARES)] for _ in range(SQUARES)]
        self.active_tiles[7][7] = True

        self.current_board = numpy.array([["_" for _ in range(SQUARES)] for _ in range(SQUARES)])
        self.board = []
        self.blank_tile_prompt_rects = []
        self.create_blank_tile_rects()

        self.tile_font = pygame.font.Font(None, FONT_SIZE)
        self.score_font = pygame.font.Font(None, int(FONT_SIZE / 2))

        self.player_score_rect = pygame.Rect(BOARD_WIDTH + 25, 25, (1 / 6) * WINDOW_WIDTH - 30, BOARD_WIDTH / SQUARES)
        self.cpu_score_rect = pygame.Rect(BOARD_WIDTH + (1 / 6) * WINDOW_WIDTH + 5, 25, (1 / 6) * WINDOW_WIDTH - 30, BOARD_WIDTH / SQUARES)
        self.tiles_remaining_rect = pygame.Rect(BOARD_WIDTH + 25, (1 / 10) * BOARD_WIDTH + 20, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.exchange_tiles_rect = pygame.Rect(BOARD_WIDTH + 25, (4 / 10) * BOARD_WIDTH - 25, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.end_game_rect = pygame.Rect(BOARD_WIDTH + 25, (1 / 2) * BOARD_WIDTH - 25, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.reset_rack_rect = pygame.Rect(BOARD_WIDTH + 25, (3 / 5) * BOARD_WIDTH - 25, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.pass_turn_rect = pygame.Rect(BOARD_WIDTH + 25, (7 / 10) * BOARD_WIDTH - 25, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.submit_rect = pygame.Rect(BOARD_WIDTH + 25, (4 / 5) * BOARD_WIDTH - 25, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)

        self.player_score = 0
        self.cpu_score = 0

    def generate_bonus_matrix(self):

        for i in range(SQUARES):
            for j in range(SQUARES):
                if (i, j) in self.triple_word_squares:
                    self.bonus_matrix[i][j] = ("TW", "red")
                if (i, j) in self.double_word_squares:
                    self.bonus_matrix[i][j] = ("DW", "pink")
                if (i, j) in self.triple_letter_squares:
                    self.bonus_matrix[i][j] = ("TL", "blue2")
                if (i, j) in self.double_letter_squares:
                    self.bonus_matrix[i][j] = ("DL", "blue1")
                if (i, j) == (7, 7):
                    self.bonus_matrix[i][j] = ("ST", "pink")

    def create_blank_tile_rects(self):

        for i in range(SQUARES):
            row = []
            for j in range(SQUARES):
                letter_rect = pygame.Rect(j * BOARD_WIDTH / SQUARES + PADDING, i * BOARD_WIDTH / SQUARES + PADDING, BOARD_WIDTH / SQUARES - PADDING, BOARD_WIDTH / SQUARES - PADDING)
                row.append(letter_rect)
            self.board.append(row)

        index = 0
        for i in range(6):
            row = []
            for j in range(5):
                blank_tile_rect = pygame.Rect((7 / 24) * WINDOW_WIDTH + PADDING + j * (1 / 12) * WINDOW_WIDTH, (1/8) * WINDOW_WIDTH + PADDING + i * (1 / 12) * WINDOW_WIDTH,
                                              (1 / 12) * WINDOW_WIDTH - PADDING, (1 / 12) * WINDOW_WIDTH - PADDING)
                row.append((blank_tile_rect, string.ascii_lowercase[index]))
                index += 1
                if index == 26:
                    break
            self.blank_tile_prompt_rects.append(row)

    def draw_board_space(self, color, rect, text):
        pygame.draw.rect(self.screen, COLORS[color], rect)
        text = self.tile_font.render(text, True, COLORS['black'])
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def draw_board(self):
        for i in range(SQUARES):
            for j in range(SQUARES):
                if self.current_board[i][j] != "_":
                    Rack.draw_tile(self.screen, self.current_board[i][j], self.board[i][j], self.tile_font, self.score_font, self.bag)
                else:
                    if self.bonus_matrix[i][j][0] != "_":
                        self.draw_board_space(self.bonus_matrix[i][j][1], self.board[i][j], self.bonus_matrix[i][j][0])
                    else:
                        pygame.draw.rect(self.screen, COLORS['light_brown'], self.board[i][j])

    def draw_blank_tile_rects(self):
        index = 0
        for i in range(6):
            for j in range(5):
                pygame.draw.rect(self.screen, COLORS['grey'], self.blank_tile_prompt_rects[i][j][0])
                index += 1
                if index == 26:
                    return

    def draw_rects(self):
        pygame.draw.rect(self.screen, COLORS['grey'], self.player_score_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['grey'], self.cpu_score_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['grey'], self.submit_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['grey'], self.reset_rack_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['grey'], self.pass_turn_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['grey'], self.end_game_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['grey'], self.tiles_remaining_rect, border_radius=15)
        pygame.draw.rect(self.screen, COLORS['grey'], self.exchange_tiles_rect, border_radius=15)

    def print_text_one_rect(self, text, rect):
        text = self.tile_font.render(text, True, COLORS['black'])
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def print_text_all_rects(self, game_tiles):
        self.print_text_one_rect(f"YOU: {self.player_score}", self.player_score_rect)
        self.print_text_one_rect(f"CPU: {self.cpu_score}", self.cpu_score_rect)
        self.print_text_one_rect("SUBMIT WORD", self.submit_rect)
        self.print_text_one_rect("Reset Rack", self.reset_rack_rect)
        self.print_text_one_rect("Pass Turn", self.pass_turn_rect)
        self.print_text_one_rect("END GAME", self.end_game_rect)
        self.print_text_one_rect(f"Tiles Remaining: {game_tiles.get_tiles_remaining()}", self.tiles_remaining_rect)
        self.print_text_one_rect("Exchange All Tiles", self.exchange_tiles_rect)

    def read_sub_word(self, row, col, current_board, letter):

        sub_word = letter

        multiplier = self.get_word_bonus(row, col, self.bonus_matrix)

        row_below = row + 1
        letter_multiplier = self.get_letter_bonus(row, col, self.bonus_matrix)
        letter_value = self.bag.get_tile_points(letter)
        score = letter_multiplier * letter_value

        while row > 0 and current_board[row - 1][col] != "_":
            sub_word = (current_board[row - 1][col] + sub_word)
            score += self.bag.get_tile_points(current_board[row - 1][col])
            row -= 1

        while row_below < SQUARES and current_board[row_below][col] != "_":
            sub_word += current_board[row_below][col]
            score += self.bag.get_tile_points(current_board[row_below][col])
            row_below += 1

        if len(sub_word) > 1:
            return sub_word, score * multiplier
        else:
            return None, 0

    @staticmethod
    def get_letter_bonus(row, col, bonus_matrix):
        if bonus_matrix[row][col][0] == "DL":
            return 2
        elif bonus_matrix[row][col][0] == "TL":
            return 3
        else:
            return 1

    @staticmethod
    def get_word_bonus(row, col, bonus_matrix):
        if bonus_matrix[row][col][0] == "DW" or bonus_matrix[row][col][0] == "ST":
            return 2
        elif bonus_matrix[row][col][0] == "TW":
            return 3
        else:
            return 1

    def read_word(self, tiles_moved, horizontal):

        move_score = 0
        main_word_score = 0
        sub_word_scores = []
        multiplier = 1
        tiles_placed = 0

        if horizontal:
            current_board = self.current_board
        else:
            current_board = self.current_board.T
            for tile in tiles_moved:
                tile[0], tile[1] = tile[1], tile[0]

        tiles_moved.sort(key=lambda item: item[1])
        word = ""
        current_index = 0
        row, col = tiles_moved[0][0], tiles_moved[0][1]
        start_col = col - 1

        while start_col >= 0 and current_board[row][start_col] != "_":
            word = (current_board[row][start_col] + word)
            main_word_score += self.bag.get_tile_points(current_board[row][start_col])
            start_col -= 1

        while col < SQUARES:
            if current_index < len(tiles_moved) and tiles_moved[current_index][1] == col:

                multiplier *= self.get_word_bonus(row, col, self.bonus_matrix)

                sub_word, sub_score = self.read_sub_word(row, col, current_board, tiles_moved[current_index][3])
                sub_word_scores.append(sub_score)

                if sub_word is not None:
                    if not self.dictionary.find_word(sub_word.upper()):
                        return False, move_score

                word += tiles_moved[current_index][3]
                letter_multiplier = self.get_letter_bonus(row, col, self.bonus_matrix)
                letter_score = self.bag.get_tile_points(tiles_moved[current_index][3])
                main_word_score += (letter_score * letter_multiplier)
                col += 1
                current_index += 1
                tiles_placed += 1

            elif current_board[row][col] != "_":
                word += current_board[row][col]
                main_word_score += self.bag.get_tile_points(current_board[row][col])
                col += 1

            elif current_index == len(tiles_moved):
                main_word_score *= multiplier
                move_score = main_word_score
                for score in sub_word_scores:
                    move_score += score

                if tiles_placed == 7:
                    move_score += 50
                break

            else:
                return False, move_score

        if not horizontal:
            for tile in tiles_moved:
                tile[0], tile[1] = tile[1], tile[0]

        return word, move_score

    @staticmethod
    def check_first_move_placement(tiles_moved):
        for tile in tiles_moved:
            if (tile[0], tile[1]) == (7, 7):
                return True
        return False

    def check_active_tile_placement(self, tiles_moved):
        for tile in tiles_moved:
            if self.active_tiles[tile[0]][tile[1]]:
                return True
        return False

    def check_valid_move(self, tiles_moved):

        # First move should intersect "S" square
        if self.first_move:
            self.first_move = False
            if not self.check_first_move_placement(tiles_moved):
                return False

        if len(tiles_moved) == 0:
            return False

        # Check to see if existing tile is already placed in any position
        for tile in tiles_moved:
            if self.current_board[tile[0]][tile[1]] != "_":
                return False

        # Words must connect to existing words on the board
        if not self.check_active_tile_placement(tiles_moved):
            return False

        # This checks to see that all tiles are placed in either 1 row or 1 column
        cols = set()
        rows = set()
        for move in tiles_moved:
            rows.add(move[0])
            cols.add(move[1])
        if len(cols) != 1 and len(rows) != 1 and len(tiles_moved) != 1:
            return False

        horizontal = True
        if len(cols) == 1:
            horizontal = False

        word, move_score = self.read_word(tiles_moved, horizontal)

        # There is ambiguity when only one tile is placed as to the direction. Fixes issue where
        # single tile placed on horizontal word causes crash because check above sets horizontal = False
        if len(cols) == 1 and len(rows) == 1:
            if word is not False and len(word) == 1:
                word, move_score = self.read_word(tiles_moved, True)

        if not word:
            return False

        if not self.dictionary.find_word(word.upper()):
            return False

        self.player_score += move_score
        return True

    def update_active_tiles(self, row, col):
        indices_to_update = [(row, col), (row, col - 1), (row - 1, col), (row, col + 1), (row + 1, col)]
        for index in indices_to_update:
            if index[0] >= SQUARES or index[0] < 0 or index[1] >= SQUARES or index[1] < 0:
                pass
            else:
                self.active_tiles[index[0]][index[1]] = True
