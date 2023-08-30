import pygame
from constants import WINDOW_WIDTH, BOARD_WIDTH, SQUARES, PADDING, FONT_SIZE
from constants import BLACK, GREY, RED, LIGHT_BROWN, PINK, BLUE, DARK_BLUE
from bag import TilesBag
from board import GameBoard

pygame.init()

game_tiles = TilesBag()
player_tiles = []
screen = pygame.display.set_mode((WINDOW_WIDTH, BOARD_WIDTH))
pygame.display.set_caption("Justin's Scrabble")

tile_font = pygame.font.Font(None, FONT_SIZE)
score_font = pygame.font.Font(None, int(FONT_SIZE/2))
board = GameBoard()

player_score = 999
cpu_score = 0

player_score_rect = pygame.Rect(BOARD_WIDTH + 25, 25, (1 / 6) * WINDOW_WIDTH - 30, BOARD_WIDTH / SQUARES)
cpu_score_rect = pygame.Rect(BOARD_WIDTH + (1 / 6) * WINDOW_WIDTH + 5, 25, (1 / 6) * WINDOW_WIDTH - 30, BOARD_WIDTH / SQUARES)

running = True
active_rect = None
letter = tile_font.render('A', True, BLACK)
while running:

    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(SQUARES):
                    for j in range(SQUARES):
                        if board.board[i][j].collidepoint(event.pos):
                            active_rect = board.board[i][j]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_rect = None

        if event.type == pygame.MOUSEMOTION:
            if active_rect is not None:
                active_rect.move_ip(event.rel)

    for i in range(SQUARES):
        for j in range(SQUARES):
            if (i, j) in board.triple_word_squares:
                pygame.draw.rect(screen, RED, board.board[i][j])
            elif (i, j) in board.triple_letter_squares:
                pygame.draw.rect(screen, DARK_BLUE, board.board[i][j])
            elif (i, j) in board.double_letter_squares:
                pygame.draw.rect(screen, BLUE, board.board[i][j])
            elif (i, j) in board.double_word_squares:
                pygame.draw.rect(screen, PINK, board.board[i][j])
            else:
                pygame.draw.rect(screen, LIGHT_BROWN, board.board[i][j])

            screen.blit(letter, (board.board[i][j].x + 0.5 * (BOARD_WIDTH / SQUARES - PADDING) - 0.25 * FONT_SIZE, board.board[i][j].y + + 0.5 * (BOARD_WIDTH / SQUARES - PADDING) - 0.25 * FONT_SIZE))

    pygame.draw.rect(screen, GREY, player_score_rect)
    pygame.draw.rect(screen, GREY, cpu_score_rect)

    player_score_text = score_font.render(f"YOU: {player_score}", True, BLACK)
    text_rect = player_score_text.get_rect(center=player_score_rect.center)
    screen.blit(player_score_text, text_rect)

    cpu_score_text = score_font.render(f"CPU: {cpu_score}", True, BLACK)
    text_rect = cpu_score_text.get_rect(center=cpu_score_rect.center)
    screen.blit(cpu_score_text, text_rect)

    pygame.display.update()

pygame.quit()
