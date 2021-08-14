import pygame
import sys
from pygame.locals import *
import numpy as np

pygame.init()
width = 600
height = 600
line_width = 15
circle_radius = 50
circle_width = 15
cross_width = 25
space = 55
board_rows = 3
board_cols = 3
bg_color = (28, 170, 156)
line_color = (23, 145, 135)
circle_color = (240, 230, 200)
cross_color = (66, 66, 66)

player = 1
game_over = False

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("TIC TAC TOE by Frank")
screen.fill(bg_color)

# board
board = np.zeros((board_rows, board_cols))


def available_square(row, col):
    return board[row][col] == 0


def mark_square(row, col, player):
    board[row][col] = player


def is_board_full():
    not_full = True
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 0:
                return False
    return True


# draw lines - horizontal and vertical
def draw_line():
    pygame.draw.line(screen, line_color, (0, 200), (600, 200), line_width)
    pygame.draw.line(screen, line_color, (0, 400), (600, 400), line_width)
    pygame.draw.line(screen, line_color, (200, 0), (200, 600), line_width)
    pygame.draw.line(screen, line_color, (400, 0), (400, 600), line_width)


def draw_figures():
    for row in range(board_rows):
        for col in range(board_cols):
            if board[row][col] == 1:
                pygame.draw.circle(screen, circle_color, (int(col * 200 + 100), int(row * 200 + 100)), circle_radius,
                                   circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, cross_color, (col * 200 + space, row * 200 + 200 - space),
                                 (col * 200 + 200 - space, row * 200 + space), cross_width)
                pygame.draw.line(screen, cross_color, (col * 200 + space, row * 200 + space),
                                 (col * 200 + 200 - space, row * 200 + 200 - space), cross_width)


def check_win(player):
    # vertical check
    for col in range(board_cols):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True

    # horizontal check
    for row in range(board_rows):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True

    # asc diagonal check
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        ascending_diagonal(player)
        return True

    # desc diagonal check
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        descending_diagonal(player)
        return True

    return False


def draw_vertical_winning_line(col, player):
    pos_x = col * 200 + 100

    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line(screen, color, (pos_x, 15), (pos_x, height - 15), 15)


def draw_horizontal_winning_line(row, player):
    pos_y = row * 200 + 100

    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line(screen, color, (15, pos_y), (width - 15, pos_y), 15)


def ascending_diagonal(player):
    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line(screen, color, (15, height - 15), (width - 15, 15), 15)


def descending_diagonal(player):
    if player == 1:
        color = circle_color
    elif player == 2:
        color = cross_color

    pygame.draw.line(screen, color, (15, 15), (width - 15, height - 15), 15)


def restart():
    screen.fill(bg_color)
    draw_line()

    for row in range(board_rows):
        for col in range(board_cols):
            board[row][col] = 0


draw_line()


# event loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN and not game_over:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            clicked_row = int(mouse_y // 200)
            clicked_col = int(mouse_x // 200)

            if available_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                    player = 2
                elif player == 2:
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                    player = 1

                draw_figures()

        if event.type == KEYDOWN:
            if event.key == K_r:
                restart()
                player = 1
                game_over = False

    pygame.display.update()
    clock.tick(60)
