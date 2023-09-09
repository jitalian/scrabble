import copy
import string
import time

import pygame
from constants import WINDOW_WIDTH, BOARD_WIDTH
from bag import TilesBag
from board import GameBoard
from rack import Rack
from words import Trie
from computer_player import ComputerPlayer

pygame.init()
pygame.display.set_caption("Justin's Scrabble")

word_dictionary = Trie("blanks_dict.txt")
game_tiles = TilesBag()
screen = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH))
board = GameBoard(screen, game_tiles, word_dictionary)
player_tiles = Rack(game_tiles, screen, board, word_dictionary)
player_tiles.tiles = ['*', 'O', 'B', 'C', 'U', 'N', 'E']
cpu_tiles = Rack(game_tiles, screen, board, word_dictionary)

computer_player = ComputerPlayer(board, cpu_tiles, word_dictionary, game_tiles)


def end_game(player_skip, cpu_skip, player_rack, cpu_rack):
    if player_skip and cpu_skip:
        return True

    if len(cpu_rack) == 0:
        return True

    count_empty = 0
    for tile in player_rack:
        if tile == "_":
            count_empty += 1

    if count_empty == 7:
        return True


running = True
active_rect = None
player_move = True

while running:

    screen.fill("black")
    player_pass = False
    cpu_pass = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
                    player_pass = True
                    player_move *= -1

                if board.end_game_rect.collidepoint(event.pos):
                    running = False

                if board.exchange_tiles_rect.collidepoint(event.pos):
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
    if player_move == -1:
        # print(player_tiles.tiles)
        if not computer_player.cpu_move():
            cpu_pass = True
        player_move *= -1

    if end_game(player_pass, cpu_pass, player_tiles.tiles, cpu_tiles.tiles):
        running = False

pygame.quit()
