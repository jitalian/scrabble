import pygame
from constants import WINDOW_WIDTH, BOARD_WIDTH
from bag import TilesBag
from board import GameBoard
from rack import Rack
from words import Trie

pygame.init()
pygame.display.set_caption("Justin's Scrabble")

word_dictionary = Trie("word_list.txt")
game_tiles = TilesBag()
screen = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH))
board = GameBoard(screen, game_tiles, word_dictionary)
player_tiles = Rack(game_tiles, screen, board, word_dictionary)

running = True
active_rect = None
player_move = True


def cpu_move():
    pass


while running:

    screen.fill("black")

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
                    pass

                if board.end_game_rect.collidepoint(event.pos):
                    running = False

                if board.exchange_tiles_rect.collidepoint(event.pos):
                    player_tiles.exchange_tiles()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_rect = None

        if event.type == pygame.MOUSEMOTION:
            if active_rect is not None:
                active_rect.move_ip(event.rel)

    board.draw_board()
    board.draw_rects()
    board.print_text_all_rects(game_tiles)
    player_tiles.draw_rack()

    pygame.display.update()
    if player_move == -1:
        cpu_move()
        player_move *= -1

pygame.quit()
