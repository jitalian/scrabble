from constants import BOARD_WIDTH, WINDOW_WIDTH, SQUARES, PADDING, FONT_SIZE, GREY, BLACK, RED, DARK_BLUE, BLUE, PINK, LIGHT_BROWN
import pygame
from rack import Rack


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

        self.allowed_tiles = [["*" for _ in range(SQUARES)] for _ in range(SQUARES)]

        self.current_board = [["_" for _ in range(SQUARES)] for _ in range(SQUARES)]
        self.board = []
        for i in range(SQUARES):
            row = []
            for j in range(SQUARES):
                letter_rect = pygame.Rect(j * BOARD_WIDTH / SQUARES + PADDING, i * BOARD_WIDTH / SQUARES + PADDING, BOARD_WIDTH / SQUARES - PADDING, BOARD_WIDTH / SQUARES - PADDING)
                row.append(letter_rect)
            self.board.append(row)

        self.tile_font = pygame.font.Font(None, FONT_SIZE)
        self.score_font = pygame.font.Font(None, int(FONT_SIZE / 2))
        self.player_score_rect = pygame.Rect(BOARD_WIDTH + 25, 25, (1 / 6) * WINDOW_WIDTH - 30, BOARD_WIDTH / SQUARES)
        self.cpu_score_rect = pygame.Rect(BOARD_WIDTH + (1 / 6) * WINDOW_WIDTH + 5, 25, (1 / 6) * WINDOW_WIDTH - 30, BOARD_WIDTH / SQUARES)
        self.submit_rect = pygame.Rect(BOARD_WIDTH + 25, (4 / 5) * BOARD_WIDTH, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.reset_rack_rect = pygame.Rect(BOARD_WIDTH + 25, (3 / 5) * BOARD_WIDTH, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.pass_turn_rect = pygame.Rect(BOARD_WIDTH + 25, (7 / 10) * BOARD_WIDTH, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.end_game_rect = pygame.Rect(BOARD_WIDTH + 25, (1 / 2) * BOARD_WIDTH, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.tiles_remaining_rect = pygame.Rect(BOARD_WIDTH + 25, (1 / 10) * BOARD_WIDTH + 20, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)
        self.exchange_tiles_rect = pygame.Rect(BOARD_WIDTH + 25, (4 / 10) * BOARD_WIDTH, (1 / 3) * WINDOW_WIDTH - 50, BOARD_WIDTH / SQUARES)

        self.player_score = 0
        self.cpu_score = 0

    def draw_board(self):
        for i in range(SQUARES):
            for j in range(SQUARES):
                if self.current_board[i][j] != "_":
                    Rack.draw_tile(self.screen, self.current_board[i][j], self.board[i][j], self.tile_font, self.score_font, self.bag)
                else:
                    if (i, j) in self.triple_word_squares:
                        pygame.draw.rect(self.screen, RED, self.board[i][j])
                        text = self.tile_font.render('TW', True, BLACK)
                        text_rect = text.get_rect(center=self.board[i][j].center)
                        self.screen.blit(text, text_rect)
                    elif (i, j) in self.triple_letter_squares:
                        pygame.draw.rect(self.screen, DARK_BLUE, self.board[i][j])
                        text = self.tile_font.render('TL', True, BLACK)
                        text_rect = text.get_rect(center=self.board[i][j].center)
                        self.screen.blit(text, text_rect)
                    elif (i, j) in self.double_letter_squares:
                        pygame.draw.rect(self.screen, BLUE, self.board[i][j])
                        text = self.tile_font.render('DL', True, BLACK)
                        text_rect = text.get_rect(center=self.board[i][j].center)
                        self.screen.blit(text, text_rect)
                    elif (i, j) in self.double_word_squares:
                        pygame.draw.rect(self.screen, PINK, self.board[i][j])
                        text = self.tile_font.render('DW', True, BLACK)
                        text_rect = text.get_rect(center=self.board[i][j].center)
                        self.screen.blit(text, text_rect)
                    elif (i, j) == self.start:
                        pygame.draw.rect(self.screen, PINK, self.board[i][j])
                        text = self.tile_font.render('S', True, BLACK)
                        text_rect = text.get_rect(center=self.board[i][j].center)
                        self.screen.blit(text, text_rect)
                    else:
                        pygame.draw.rect(self.screen, LIGHT_BROWN, self.board[i][j])

    def draw_rects(self):
        pygame.draw.rect(self.screen, GREY, self.player_score_rect)
        pygame.draw.rect(self.screen, GREY, self.cpu_score_rect)
        pygame.draw.rect(self.screen, GREY, self.submit_rect)
        pygame.draw.rect(self.screen, GREY, self.reset_rack_rect)
        pygame.draw.rect(self.screen, GREY, self.pass_turn_rect)
        pygame.draw.rect(self.screen, GREY, self.end_game_rect)
        pygame.draw.rect(self.screen, GREY, self.tiles_remaining_rect)
        pygame.draw.rect(self.screen, GREY, self.exchange_tiles_rect)

    def print_text(self, game_tiles):
        player_score_text = self.tile_font.render(f"YOU: {self.player_score}", True, BLACK)
        text_rect = player_score_text.get_rect(center=self.player_score_rect.center)
        self.screen.blit(player_score_text, text_rect)

        cpu_score_text = self.tile_font.render(f"CPU: {self.cpu_score}", True, BLACK)
        text_rect = cpu_score_text.get_rect(center=self.cpu_score_rect.center)
        self.screen.blit(cpu_score_text, text_rect)

        submit_text = self.tile_font.render("SUBMIT WORD", True, BLACK)
        text_rect = submit_text.get_rect(center=self.submit_rect.center)
        self.screen.blit(submit_text, text_rect)

        reset_text = self.tile_font.render("Reset Rack", True, BLACK)
        text_rect = reset_text.get_rect(center=self.reset_rack_rect.center)
        self.screen.blit(reset_text, text_rect)

        pass_text = self.tile_font.render("Pass Turn", True, BLACK)
        text_rect = pass_text.get_rect(center=self.pass_turn_rect.center)
        self.screen.blit(pass_text, text_rect)

        end_text = self.tile_font.render("END GAME", True, BLACK)
        text_rect = end_text.get_rect(center=self.end_game_rect.center)
        self.screen.blit(end_text, text_rect)

        tiles_remaining_text = self.tile_font.render(f"Tiles Remaining: {game_tiles.get_tiles_remaining()}", True, BLACK)
        text_rect = tiles_remaining_text.get_rect(center=self.tiles_remaining_rect.center)
        self.screen.blit(tiles_remaining_text, text_rect)

        exchange_text = self.tile_font.render("Exchange All Tiles", True, BLACK)
        text_rect = exchange_text.get_rect(center=self.exchange_tiles_rect.center)
        self.screen.blit(exchange_text, text_rect)

    def generate_word_lanes(self):
        pass

    def check_valid_placement(self, tiles_moved):

        if len(tiles_moved) == 0:
            return False

        for index in tiles_moved:
            if self.current_board[index[0]][index[1]] != "_":
                return False

        # This checks to see that all tiles are placed in either 1 row or 1 column
        cols = set()
        rows = set()
        for move in tiles_moved:
            rows.add(move[0])
            cols.add(move[1])

        if len(cols) != 1 and len(rows) != 1:
            return False

        # TODO There needs to be a check for when only one tile is placed because both rows and cols == 1
        horizontal = True
        if len(cols) == 1:
            horizontal = False

        tiles_moved.sort(key=lambda item: item[1])
        word = ""
        current_index = 0
        row, col = tiles_moved[0][0], tiles_moved[0][1]
        if horizontal:
            start_col = col - 1
            while start_col >= 0 and self.current_board[row][start_col] != "_":
                word = (self.current_board[row][start_col] + word)
                start_col -= 1

            while col < SQUARES:
                if current_index < len(tiles_moved) and tiles_moved[current_index][1] == col:
                    word += tiles_moved[current_index][3]
                    col += 1
                    current_index += 1
                elif self.current_board[row][col] != "_":
                    word += self.current_board[row][col]
                    col += 1
                elif current_index == len(tiles_moved):
                    break
                else:
                    return False

        if not self.dictionary.find_word(word):
            return False

        return True

    def update_allowed_tiles(self):
        pass

    def score_word(self, board):
        pass
