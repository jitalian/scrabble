from constants import BOARD_WIDTH, SQUARES, WINDOW_WIDTH, DARK_GREY, YELLOW, PADDING, FONT_SIZE, BLACK
import pygame


class Rack:
    def __init__(self, game_tiles, screen, board):
        self.screen = screen
        self.game_tiles = game_tiles
        self.board = board
        self.tiles = [self.game_tiles.get_random_tile() for i in range(7)]
        self.tile_rects = []
        self.generate_tile_rects()

    def generate_tile_rects(self, reset=False):
        if reset is True:
            self.tile_rects = []
        x_pos = BOARD_WIDTH + PADDING + 27
        y_pos = (7 / 8) * BOARD_WIDTH + 20
        for i in range(len(self.tiles)):
            tile_size = BOARD_WIDTH / 18
            tile_rect = pygame.Rect(x_pos, y_pos, tile_size, tile_size)
            self.tile_rects.append(tile_rect)
            x_pos += (tile_size + 3 * PADDING)

    @staticmethod
    def draw_tile(screen, tile, tile_rect, tile_font, score_font, bag):
        pygame.draw.rect(screen, YELLOW, tile_rect)
        text = tile_font.render(tile, True, BLACK)
        text_rect = text.get_rect(center=tile_rect.center)
        screen.blit(text, text_rect)

        text = score_font.render(str(bag.points[tile]), True, BLACK)
        text_rect = text.get_rect(center=(tile_rect.right - 8, tile_rect.bottom - 8))
        screen.blit(text, text_rect)

    def draw_rack(self):
        rack_rect = pygame.Rect(BOARD_WIDTH + 15, (7 / 8) * BOARD_WIDTH, (1 / 3) * WINDOW_WIDTH - 30, 1.5 * BOARD_WIDTH / SQUARES)
        pygame.draw.rect(self.screen, DARK_GREY, rack_rect)
        tile_font = pygame.font.Font(None, FONT_SIZE)
        score_font = pygame.font.Font(None, int(FONT_SIZE / 2))
        for i in range(len(self.tiles)):
            self.draw_tile(self.screen, self.tiles[i], self.tile_rects[i], tile_font, score_font, self.game_tiles)

    def exchange_tiles(self):
        for tile in self.tiles:
            self.game_tiles.tiles.append(tile)

        self.tiles = [self.game_tiles.get_random_tile() for i in range(7)]
        self.generate_tile_rects(reset=True)

    def submit_move(self):
        # TODO Check for valid move

        for i in range(len(self.tiles)):
            for j in range(SQUARES):
                for k in range(SQUARES):
                    if self.board.board[j][k].collidepoint(self.tile_rects[i].center):
                        self.board.current_board[j][k] = self.tiles[i]
                        new_tile = self.game_tiles.get_random_tile()
                        if new_tile is not None:
                            self.tiles[i] = new_tile

        self.generate_tile_rects(reset=True)

