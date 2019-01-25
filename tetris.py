#!/usr/bin/env python3
import curses
from curses import KEY_RESIZE
import random
import time


def draw_X(screen, y, x, char):
    """
    DRAW X IN SCREEN
    """
    screen.addch(y, x, ord(char), curses.A_BOLD)


def init_board(height, width):
    """
    INIT THE MATRIX DEPEND ON THE BOADR GAME
    TRUE => "X"
    FALSE => ' '
    """
    board = []
    for i in range(height):
        board.append([])
        for j in range(width):
            board[i].append(False)
    for i in range(height):
        for j in range(width):
            print(board[i][j], end='')
        print('')
    return board


def draw_board(board, screen):
    """
    DRAW MATRIX IN SCREEN
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if j == 0:
                draw_X(screen, i, j, '|')
            elif board[i][j]:
                draw_X(screen, i, j, 'X')
            else:
                draw_X(screen, i, j, ' ')


def get_collision(board, y, x):
    """
    STOP DROPPING OF X
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            if y >= len(board) or board[y][x]:
                return True
    return False


def check_lines(board):
    """
    CHEKC LINE IS FULL OF "X" OR NOT?
    """
    lines_cleared = 0
    for i in range(len(board)):
        full_line = True
        for j in range(1, len(board[i])):
            if not board[i][j]:
                full_line = False
                break
        if full_line:
            for m in range(len(board) - 1, 0, -1):
                for n in range(1, len(board[m])):
                    board[m][n] = board[m-1][n]
            for k in range(1, len(board[m])):
                board[0][k] = False
            lines_cleared += 1
    return lines_cleared


def is_game_over(board, y, x):
    """Return true if the game is over, false otherwise"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            if y + i <= 0:
                return True
    return False


def move_X(x, y, input, board, lines_Board, dims):
    """
    MOVING BY PLAYER
    """
    check = False
    if not get_collision(board, y+1, x):
        y += 1
        # MOVE LEFT
        if input == curses.KEY_LEFT and x > 1:
            if not get_collision(board, y, x-1):
                x -= 1
        # MOVE RIGHT
        elif input == curses.KEY_RIGHT and x < dims[1]//2 - 2 and x >= 1:
            if not get_collision(board, y, x+1):
                x += 1
        # MOVE UP
        elif input == curses.KEY_DOWN and y < dims[0] - 1:
            if not get_collision(board, y+1, x):
                y += 1
            else:
                check = True
    else:
        check = True
    return check, x, y


def out_game(screen):
    screen.clear()
    screen.addstr(2, 1, 'CHANGE SIZE IS NOT GOOD FOR YOU', curses.A_BOLD)
    screen.addstr(4, 1, 'GAME WILL BE BROKEN OUT IN 5 SECONDS', curses.A_BOLD)
    screen.refresh()
    time.sleep(5)
    curses.endwin()
    exit(0)


def init_game():
    # set up game
    screen = curses.initscr()
    curses.noecho()
    curses.curs_set(0)
    screen.keypad(1)
    screen.nodelay(1)
    return screen


def set_background(screen, dims):
    for y in range(dims[0]):
        screen.addch(y, dims[1]//2 - 1, ord('|'), curses.A_BOLD)  # drop down


def playing_game():
    # set up game
    screen = init_game()

    # set up bachground game
    dims = screen.getmaxyx()
    set_background(screen, dims)

    # inut matrix of board game
    board = init_board(dims[0], dims[1]//2-1)

    # set score and random dropping
    score = 0
    y = 0
    x = random.randrange(1, dims[1]//2 - 1, 1)
    game_over = False
    index_list = []

    # running game
    while not game_over:

        lines_Board = dims[0]
        width_Board = dims[1]

        # het input of player
        input = screen.getch()

        # exit game when player resized the screen
        if input == KEY_RESIZE:
            out_game(screen)

        # exit game by input of player
        if input == ord('q'):
            game_over = True

        board[y][x] = False

        draw_X(screen, y, x, 'X')

        # moving with input of player
        if y < lines_Board - 1:
            check, x, y = move_X(x, y, input, board, lines_Board, dims)

        board[y][x] = True
        # set score
        score = score + check_lines(board)

        # set up board
        draw_board(board, screen)

        # draw X
        draw_X(screen, y, x, "X")

        # check end game
        if check or y >= lines_Board - 1:
            game_over = is_game_over(board, y, x)
            index_list.append([y, x])
            x = random.randrange(1, dims[1]//2 - 1, 1)
            y = 0
        screen.addstr(dims[0]//2, dims[1]//2 + dims[1]//4 - 4,
                      "SCORE: %s" % score, curses.A_BOLD)
        screen.timeout(200)

    # throw message
    screen.clear()
    screen.addstr(2, 1, 'GAME OVER', curses.A_BOLD)
    screen.refresh()
    time.sleep(5)
    curses.endwin()


playing_game()
