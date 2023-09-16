import pygame
from constants import WINDOW_WIDTH, BOARD_WIDTH
from bag import TilesBag
from board import GameBoard
from player_rack import PlayerRack
from words import Trie
from computer_player import ComputerPlayer
import sys


def run_game():
    pygame.init()
    pygame.display.set_caption("Justin's Scrabble")
    screen = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH))
    board = GameBoard(screen, None, None)

    board.information_screen()

    program_running = True
    while program_running:

        board.welcome_screen()

        active_rect = None
        player_move = True

        word_dictionary = Trie("blanks_dict.txt")
        game_tiles = TilesBag()

        board.dictionary = word_dictionary
        board.game_tiles = game_tiles

        player_tiles = PlayerRack(game_tiles, screen, board, word_dictionary)
        computer_player = ComputerPlayer(board, game_tiles, word_dictionary, game_tiles)

        player_pass = 0
        cpu_pass = 0

        game_running = True
        while game_running:

            screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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
                                player_pass = 0

                        if board.pass_turn_rect.collidepoint(event.pos):
                            player_pass += 1
                            player_move *= -1
                            board.player_last_move_text = "TURN PASSED!"

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
            board.draw_game_panel()
            player_tiles.draw_rack()
            pygame.display.update()

            if player_move == -1 and player_tiles.tiles.count("_") != 7:
                cpu_move = computer_player.cpu_move()
                player_move *= -1
                if not cpu_move:
                    cpu_pass += 1
                    board.cpu_last_move_text = "TURN PASSED!"
                else:
                    cpu_pass = 0

            if board.check_end_game(player_pass, cpu_pass, player_tiles.tiles, computer_player.tiles):
                game_running = False

        board.end_screen(player_tiles)
        board = GameBoard(screen, None, None)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_game()
