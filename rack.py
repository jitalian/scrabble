from constants import BOARD_WIDTH, SQUARES, WINDOW_WIDTH, COLORS, PADDING, FONT_SIZE
import pygame


class Rack:
    """Class representing rack of tiles"""
    def __init__(self, game_tiles, screen, board, words):
        self.words = words
        self.screen = screen
        self.game_tiles = game_tiles
        self.board = board
        self.tiles = [self.game_tiles.get_random_tile() for i in range(7)]
        self.tile_rects = []
        self.generate_tile_rects()
        self.blank_prompt_text = "CHOOSE BLANK"

    def generate_tile_rects(self, reset=False):
        """Generates Rect objects for current tile rack."""
        if reset is True:
            self.tile_rects = []
        x_pos = BOARD_WIDTH + PADDING + (1/45) * WINDOW_WIDTH
        y_pos = (7/8) * BOARD_WIDTH + (1/60) * WINDOW_WIDTH
        for i in range(len(self.tiles)):
            tile_size = BOARD_WIDTH / 18
            tile_rect = pygame.Rect(x_pos, y_pos, tile_size, tile_size)
            self.tile_rects.append(tile_rect)
            x_pos += (tile_size + (WINDOW_WIDTH/400) * PADDING)

    def blank_tile_prompt(self):
        """Prompts the user to select a blank tile. Returns the Rect object
        associated with what the user selects"""
        prompt = True
        while prompt:
            self.screen.fill("black")
            self.board.draw_board()
            self.board.draw_rects()
            self.board.print_text_all_rects(self.game_tiles)
            pygame.draw.rect(self.screen, COLORS['black'], self.board.blank_prompt_rect_background)
            pygame.draw.rect(self.screen, COLORS['red'], self.board.pick_blank_prompt, border_radius=15)
            self.board.print_text_one_rect(self.blank_prompt_text, self.board.pick_blank_prompt, self.board.tile_font)
            self.draw_rack()
            self.board.draw_blank_tile_rects()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    prompt = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(6):
                            for rect in self.board.blank_tile_prompt_rects[i]:
                                if rect[0].collidepoint(event.pos):
                                    return rect[1]

            for i in range(6):
                for rect in self.board.blank_tile_prompt_rects[i]:
                    self.draw_blank(rect[1], rect[0])

            pygame.display.update()

    def draw_blank(self, tile, tile_rect):
        """Draws given tile on given tile_rect onto the screen."""
        pygame.draw.rect(self.screen, COLORS['yellow'], tile_rect)
        text = self.board.tile_font.render(tile, True, COLORS['black'])
        text_rect = text.get_rect(center=tile_rect.center)
        self.screen.blit(text, text_rect)

    @staticmethod
    def draw_tile(screen, tile, tile_rect, tile_font, score_font, bag):
        """Draws given tile and tile points on the screen."""

        pygame.draw.rect(screen, COLORS['yellow'], tile_rect)

        if tile.isupper():
            text = tile_font.render(tile, True, COLORS['black'])
            text_rect = text.get_rect(center=tile_rect.center)
            screen.blit(text, text_rect)

            text = score_font.render(str(bag.points[tile]), True, COLORS['black'])
            text_rect = text.get_rect(center=(tile_rect.right - 8, tile_rect.bottom - 8))
            screen.blit(text, text_rect)

        else:
            text = tile_font.render(tile.upper(), True, COLORS['red'])
            text_rect = text.get_rect(center=tile_rect.center)
            screen.blit(text, text_rect)

            text = score_font.render("0", True, COLORS['red'])
            text_rect = text.get_rect(center=(tile_rect.right - 8, tile_rect.bottom - 8))
            screen.blit(text, text_rect)

    def draw_rack(self):
        """Draws the players current rack on the screen."""
        rack_rect = pygame.Rect(BOARD_WIDTH + 15, (7 / 8) * BOARD_WIDTH, (1 / 3) * WINDOW_WIDTH - 30, 1.5 * BOARD_WIDTH / SQUARES)
        pygame.draw.rect(self.screen, COLORS['dark_grey'], rack_rect, border_radius=15)
        tile_font = pygame.font.Font(None, FONT_SIZE)
        score_font = pygame.font.Font(None, int(FONT_SIZE / 2))
        for i in range(len(self.tiles)):
            if self.tiles[i] != "_":
                self.draw_tile(self.screen, self.tiles[i], self.tile_rects[i], tile_font, score_font, self.game_tiles)

    def exchange_tiles(self):
        """Exchanges the tiles and reset tile rects to their default positions."""
        for tile in self.tiles:
            self.game_tiles.tiles.append(tile)

        self.tiles = [self.game_tiles.get_random_tile() for _ in range(7)]
        self.generate_tile_rects(reset=True)

    def get_move_indices(self):
        """Determines which tiles were moved and what board space they were moved to.
        Returns a list of [row, col, rack_index, tile]."""
        tiles_moved = []
        blank_chosen = False
        for i in range(len(self.tiles)):
            for j in range(SQUARES):
                for k in range(SQUARES):
                    if self.board.board[j][k].collidepoint(self.tile_rects[i].center):
                        if self.tiles[i] == "*":
                            if blank_chosen is True:
                                self.blank_prompt_text = "CHOOSE NEXT BLANK"
                            tiles_moved.append([j, k, i, self.blank_tile_prompt()])
                            blank_chosen = True
                        else:
                            tiles_moved.append([j, k, i, self.tiles[i]])
        return tiles_moved

    def submit_move(self):
        """Submits the current move. The board class checks the validity. Returns true if the move was valid
        and false otherwise."""
        move_indices = self.get_move_indices()

        valid_move = self.board.check_valid_move(move_indices)
        if not valid_move:
            self.generate_tile_rects(reset=True)
            return False

        for i in range(len(move_indices)):
            row, col, index = move_indices[i][0], move_indices[i][1], move_indices[i][2]
            if self.tiles[index] == "*":
                self.board.current_board[row][col] = move_indices[i][3]
            else:
                self.board.current_board[row][col] = self.tiles[index]
            self.board.update_active_tiles(row, col)

            new_tile = self.game_tiles.get_random_tile()
            if new_tile is not None:
                self.tiles[index] = new_tile
            else:
                self.tiles[index] = "_"

        self.generate_tile_rects(reset=True)

        return True
