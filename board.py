from constants import BOARD_WIDTH, SQUARES, PADDING
import pygame


class GameBoard:
    def __init__(self):
        self.triple_word_squares = {(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)}
        self.triple_letter_squares = {(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5),
                                      (9, 9), (9, 13), (12, 5), (12, 9)}
        self.double_letter_squares = {(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2),
                                      (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8),
                                      (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)}
        self.double_word_squares = {(1, 1), (1, 13), (2, 2), (2, 12), (3, 3), (3, 11), (4, 4), (4, 10),
                                    (10, 4), (10, 10), (11, 3), (11, 11), (12, 2), (12, 12), (13, 1), (13, 13)}

        self.allowed_tiles = []

        self.board = []
        for i in range(SQUARES):
            row = []
            for j in range(SQUARES):
                letter_rect = pygame.Rect(j * BOARD_WIDTH / SQUARES + PADDING, i * BOARD_WIDTH / SQUARES + PADDING, BOARD_WIDTH / SQUARES - PADDING, BOARD_WIDTH / SQUARES - PADDING)
                row.append(letter_rect)
            self.board.append(row)

    def generate_word_lanes(self):
        pass

    def check_valid_word(self):
        pass

    def update_allowed_tiles(self):
        pass

    def score_word(self, board):
        pass
