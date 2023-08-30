import pygame

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BOARD_WIDTH = (2/3) * WINDOW_WIDTH
SQUARES = 15
PADDING = 2
FONT_SIZE = int(WINDOW_HEIGHT/12)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_BROWN = (234, 221, 202)
PINK = (255, 182, 193)
BLUE = (135, 206, 250)
DARK_BLUE = (0, 0, 255)


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Justin's Scrabble")

font = pygame.font.Font(None, FONT_SIZE)


triple_word_squares = {(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)}
triple_letter_squares = {(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9), (9, 13), (12, 5), (12, 9)}
double_letter_squares = {(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3), (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)}
double_word_squares = {(1, 1), (1, 13), (2, 2), (2, 12), (3, 3), (3, 11), (4, 4), (4, 10), (10, 4), (10, 10), (11, 3), (11, 11), (12, 2), (12, 12), (13, 1), (13, 13)}

board = []
for i in range(SQUARES):
    row = []
    for j in range(SQUARES):
        letter_rect = pygame.Rect(j * BOARD_WIDTH/SQUARES + PADDING, i * BOARD_WIDTH/SQUARES + PADDING, BOARD_WIDTH/SQUARES - PADDING, BOARD_WIDTH/SQUARES - PADDING)
        row.append(letter_rect)
    board.append(row)

running = True
active_rect = None
letter = font.render('A', True, BLACK)
while running:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(SQUARES):
                    for j in range(SQUARES):
                        if board[i][j].collidepoint(event.pos):
                            active_rect = board[i][j]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_rect = None

        if event.type == pygame.MOUSEMOTION:
            if active_rect is not None:
                active_rect.move_ip(event.rel)

    for i in range(SQUARES):
        for j in range(SQUARES):
            if (i, j) in triple_word_squares:
                pygame.draw.rect(screen, RED, board[i][j])
            elif (i, j) in triple_letter_squares:
                pygame.draw.rect(screen, DARK_BLUE, board[i][j])
            elif (i, j) in double_letter_squares:
                pygame.draw.rect(screen, BLUE, board[i][j])
            elif (i, j) in double_word_squares:
                pygame.draw.rect(screen, PINK, board[i][j])
            else:
                pygame.draw.rect(screen, LIGHT_BROWN, board[i][j])

            screen.blit(letter, (board[i][j].x + 0.5 * (BOARD_WIDTH/SQUARES - PADDING) - 0.25 * FONT_SIZE, board[i][j].y + + 0.5 * (BOARD_WIDTH/SQUARES - PADDING) - 0.25 * FONT_SIZE))

    pygame.draw.rect(screen, LIGHT_BROWN, pygame.Rect(BOARD_WIDTH + 25, 25, (1/3) * WINDOW_WIDTH - 50, WINDOW_HEIGHT/SQUARES))

    pygame.display.update()

pygame.quit()


