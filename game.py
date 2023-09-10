import pygame
from constants import WINDOW_WIDTH, BOARD_WIDTH, COLORS, FONT_SIZE
from bag import TilesBag
from board import GameBoard
from rack import Rack
from words import Trie
from computer_player import ComputerPlayer


def end_game(player_skip, cpu_skip, player_rack, cpu_rack):
    if player_skip == 2 and cpu_skip == 2:
        return True

    if len(cpu_rack) == 0:
        return True

    count_empty = player_rack.count("_")
    if count_empty == 7:
        return True


def print_text_one_rect(text, rect, font, screen, color):
    text = font.render(text, True, COLORS[color])
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)


def welcome_screen(screen):
    scrabble_rect = pygame.Rect(0.125 * WINDOW_WIDTH, 0.15 * BOARD_WIDTH, 0.75 * WINDOW_WIDTH, 0.4 * BOARD_WIDTH)
    quit_rect = pygame.Rect(0.125 * WINDOW_WIDTH, 0.6 * BOARD_WIDTH, 0.35 * WINDOW_WIDTH, 0.2 * BOARD_WIDTH)
    begin_game_rect = pygame.Rect(0.525 * WINDOW_WIDTH, 0.6 * BOARD_WIDTH, 0.35 * WINDOW_WIDTH, 0.2 * BOARD_WIDTH)
    loading_rect = pygame.Rect(0.125 * WINDOW_WIDTH, 0.15 * BOARD_WIDTH, 0.75 * WINDOW_WIDTH, 0.4 * BOARD_WIDTH)

    welcome = True

    while welcome:
        screen.fill("black")
        pygame.draw.rect(screen, COLORS['dark_grey'], scrabble_rect, border_radius=10)
        pygame.draw.rect(screen, COLORS['dark_grey'], quit_rect, border_radius=10)
        pygame.draw.rect(screen, COLORS['dark_grey'], begin_game_rect, border_radius=10)

        print_text_one_rect("SCRABBLE", scrabble_rect, pygame.font.Font(None, int(FONT_SIZE * 5)), screen, "dark_red")
        print_text_one_rect("QUIT GAME", quit_rect, pygame.font.Font(None, int(FONT_SIZE * 2)), screen, "black")
        print_text_one_rect("BEGIN GAME", begin_game_rect, pygame.font.Font(None, int(FONT_SIZE * 2)), screen, "black")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if begin_game_rect.collidepoint(event.pos):
                        welcome = False
                        screen.fill("black")
                        print_text_one_rect("LOADING...", loading_rect, pygame.font.Font(None, int(FONT_SIZE * 5)), screen, "dark_red")
                        pygame.display.update()

                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()


def information_screen(screen):
    line1_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 0.125 * BOARD_WIDTH)
    line2_rect = pygame.Rect(0, 0.125 * BOARD_WIDTH, WINDOW_WIDTH, 0.125 * BOARD_WIDTH)
    line3_rect = pygame.Rect(0, 0.25 * BOARD_WIDTH, WINDOW_WIDTH, 0.125 * BOARD_WIDTH)
    line4_rect = pygame.Rect(0, 0.375 * BOARD_WIDTH, WINDOW_WIDTH, 0.125 * BOARD_WIDTH)
    line5_rect = pygame.Rect(0, 0.5 * BOARD_WIDTH, WINDOW_WIDTH, 0.125 * BOARD_WIDTH)
    line6_rect = pygame.Rect(0, 0.625 * BOARD_WIDTH, WINDOW_WIDTH, 0.125 * BOARD_WIDTH)
    line7_rect = pygame.Rect(0, 0.75 * BOARD_WIDTH, WINDOW_WIDTH, 0.125 * BOARD_WIDTH)
    line8_rect = pygame.Rect(0.35 * WINDOW_WIDTH, 0.875 * BOARD_WIDTH, 0.3 * WINDOW_WIDTH, 0.1 * BOARD_WIDTH)

    information = True
    while information:
        screen.fill("black")
        pygame.draw.rect(screen, COLORS['black'], line1_rect)
        pygame.draw.rect(screen, COLORS['black'], line2_rect)
        pygame.draw.rect(screen, COLORS['black'], line3_rect)
        pygame.draw.rect(screen, COLORS['black'], line4_rect)
        pygame.draw.rect(screen, COLORS['black'], line5_rect)
        pygame.draw.rect(screen, COLORS['black'], line6_rect)
        pygame.draw.rect(screen, COLORS['black'], line7_rect)
        pygame.draw.rect(screen, COLORS['blue1'], line8_rect, border_radius=15)

        print_text_one_rect("WARNING:", line1_rect, pygame.font.Font(None, int(FONT_SIZE * 2)), screen, "red")
        print_text_one_rect("This game doesn't use the official scrabble dictionary.", line2_rect, pygame.font.Font(None, int(FONT_SIZE * 1.5)), screen, "dark_grey")
        print_text_one_rect("It uses the the open-source wordnik list found at:", line3_rect, pygame.font.Font(None, int(FONT_SIZE * 1.5)), screen, "dark_grey")
        print_text_one_rect("https://github.com/wordnik/wordlist", line4_rect, pygame.font.Font(None, int(FONT_SIZE * 1.5)), screen, "dark_grey")
        print_text_one_rect("As a result there are many non-official words in play.", line5_rect, pygame.font.Font(None, int(FONT_SIZE * 1.5)), screen, "dark_grey")
        print_text_one_rect("For this game the computer player will always play a", line6_rect, pygame.font.Font(None, int(FONT_SIZE * 1.5)), screen, "dark_grey")
        print_text_one_rect("highest scoring move, but is limited to one blank tile.", line7_rect, pygame.font.Font(None, int(FONT_SIZE * 1.5)), screen, "dark_grey")
        print_text_one_rect("CONTINUE", line8_rect, pygame.font.Font(None, int(FONT_SIZE * 1.5)), screen, "black")
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if line8_rect.collidepoint(event.pos):
                        information = False


def run_game():
    pygame.init()
    pygame.display.set_caption("Justin's Scrabble")
    screen = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH))

    information_screen(screen)

    program_running = True

    while program_running:

        welcome_screen(screen)

        game_running = True
        active_rect = None
        player_move = True

        word_dictionary = Trie("blanks_dict.txt")
        game_tiles = TilesBag()

        board = GameBoard(screen, game_tiles, word_dictionary)
        player_tiles = Rack(game_tiles, screen, board, word_dictionary)
        # player_tiles.tiles = ['H', 'A', 'T', '*', 'U', 'N', 'E']
        cpu_tiles = Rack(game_tiles, screen, board, word_dictionary)

        computer_player = ComputerPlayer(board, cpu_tiles, word_dictionary, game_tiles)

        while game_running:

            screen.fill("black")
            player_pass = 0
            cpu_pass = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i in range(len(player_tiles.tiles)):
                            if player_tiles.tile_rects[i].collidepoint(event.pos):
                                active_rect = player_tiles.tile_rects[i]

                        if board.reset_rack_rect.collidepoint(event.pos):
                            player_tiles.generate_tile_rects(reset=True)

                        if board.submit_rect.collidepoint(event.pos):
                            if player_tiles.submit_move():
                                player_move *= -1

                        if board.pass_turn_rect.collidepoint(event.pos):
                            player_pass += 1
                            player_move *= -1

                        if board.end_game_rect.collidepoint(event.pos):
                            game_running = False

                        if board.exchange_tiles_rect.collidepoint(event.pos):
                            player_pass += 1
                            player_move *= -1
                            player_tiles.exchange_tiles()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        active_rect = None

                if event.type == pygame.MOUSEMOTION:
                    if active_rect is not None:
                        active_rect.move_ip(event.rel)

            screen.fill("black")
            board.draw_board()
            board.draw_rects()
            board.print_text_all_rects(game_tiles)
            player_tiles.draw_rack()

            pygame.display.update()
            if player_move == -1 and player_tiles.tiles.count("_") != 7:
                if not computer_player.cpu_move():
                    cpu_pass += 1
                player_move *= -1

            if end_game(player_pass, cpu_pass, player_tiles.tiles, cpu_tiles.tiles):
                game_running = False

        end_screen = True

        while end_screen:
            if board.cpu_score > board.player_score:
                text = f"COMPUTER WINS WITH {board.cpu_score} POINTS!"
            else:
                text = f"YOU WIN WITH {board.player_score} POINTS!"

            winner_rect = pygame.Rect(0.05 * WINDOW_WIDTH, 0.2 * WINDOW_WIDTH, 0.9 * WINDOW_WIDTH, 0.2 * BOARD_WIDTH)
            main_menu_rect = pygame.Rect(0.4 * WINDOW_WIDTH, 0.2 * WINDOW_WIDTH + 0.225 * BOARD_WIDTH, 0.2 * WINDOW_WIDTH, 0.1 * BOARD_WIDTH)
            pygame.draw.rect(screen, COLORS["dark_red"], winner_rect, border_radius=20)
            pygame.draw.rect(screen, COLORS["black"], main_menu_rect, border_radius=20)

            print_text_one_rect(text, winner_rect, pygame.font.Font(None, int(FONT_SIZE * 2)), screen, "black")
            print_text_one_rect("Main Menu", main_menu_rect, pygame.font.Font(None, int(FONT_SIZE)), screen, "grey")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if main_menu_rect.collidepoint(event.pos):
                            end_screen = False

    pygame.quit()


if __name__ == "__main__":
    run_game()
