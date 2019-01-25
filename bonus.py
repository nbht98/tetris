#!/usr/bin/env python3
import curses
from curses import KEY_RESIZE
import random
import time


def get_new_block(block):
    if len(block) == 2:
        return [[False, False],
                [False, False],
                [False, False]]
    else:
        return [[False, False, False], [False, False, False]]


def change_rotation(block1, block2):
    if len(block1) == 2:
        block2[0][0] = block1[1][0]
        block2[0][1] = block1[0][0]
        block2[1][0] = block1[1][1]
        block2[1][1] = block1[0][1]
        block2[2][0] = block1[1][2]
        block2[2][1] = block1[0][2]
    else:
        block2[0][0] = block1[2][0]
        block2[0][1] = block1[1][0]
        block2[0][2] = block1[0][0]
        block2[1][0] = block1[2][1]
        block2[1][1] = block1[1][1]
        block2[1][2] = block1[0][1]
    return block2


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
            elif i == len(board) - 1:
                draw_X(screen, i, j, '#')
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


def get_block_collision(board, block, y, x):
    if y >= len(board) - len(block) or x >= len(board[0]) - len(block[0]) + 1:
        return True
    for i in range(len(block)):
        for j in range(len(block[i])):
            if board[y + i][x + j]:
                if block[i][j]:
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


def move_X(block, x, y, input, board, lines_Board, dims):
    """
    MOVING BY PLAYER
    """
    check = False
    if not get_block_collision(board, block, y+1, x):
        y += 1
        # MOVE LEFT
        if input == curses.KEY_LEFT and x > 1:
            if not get_block_collision(board, block, y, x-1):
                x -= 1
        # MOVE RIGHT
        elif input == curses.KEY_RIGHT:
            if x < dims[1]//2 - len(block[0]) and x >= 1:
                if not get_block_collision(board, block, y, x+1):
                    x += 1
        # MOVE UP
        elif input == curses.KEY_UP:
            blocktmp = get_new_block(block)
            newblock = change_rotation(block, blocktmp)
            if not get_block_collision(board, newblock, y, x+1):
                block = newblock
        elif input == curses.KEY_DOWN and y < dims[0] - len(block):
            if not get_block_collision(board, block, y+1, x):
                y += 1
            else:
                check = True
    else:
        check = True
    return check, block, x, y


def out_game(screen):
    screen.clear()
    screen.addstr(2, 1, 'CHANGE SIZE IS NOT GOOD FOR YOU', curses.A_BOLD)
    screen.addstr(4, 1, 'GAME WILL BE BROKEN OUT IN 5 SECONDS', curses.A_BOLD)
    screen.refresh()
    time.sleep(5)
    curses.endwin()
    exit(0)


def build_block():
    block_L = [[False, False, True], [True, True, True]]
    block_J = [[True, False, False], [True, True, True]]
    block_I = [[False, False, False], [True, True, True]]
    block_O = [[True, True, False], [True, True, False]]
    dict_block = {1: block_L, 2: block_J, 3: block_I, 4: block_O}
    type_block = dict_block[random.randint(1, 4)]
    return type_block


def draw_Xs(screen, block, y, x):
    """
    DRAW X IN SCREEN
    """
    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j]:
                draw_X(screen, y + i, x + j, 'X')
    # screen.addch(y, x, ord(dic_draw[block[0][0]]), curses.A_BOLD)
    # screen.addch(y, x + 1, ord(dic_draw[block[0][1]]), curses.A_BOLD)
    # screen.addch(y, x + 2, ord(dic_draw[block[0][2]]), curses.A_BOLD)
    # screen.addch(y + 1, x, ord(dic_draw[block[1][0]]), curses.A_BOLD)
    # screen.addch(y + 1, x + 1, ord(dic_draw[block[1][1]]), curses.A_BOLD)
    # screen.addch(y + 1, x + 2, ord(dic_draw[block[1][2]]), curses.A_BOLD)


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
        screen.addch(y, dims[1]//2 - 2, ord('|'), curses.A_BOLD)


def playing_game():
    # set up game
    screen = init_game()

    # set up bachground game
    dims = screen.getmaxyx()
    set_background(screen, dims)

    # inut matrix of board game
    board = init_board(dims[0], dims[1]//2-2)

    block = build_block()
    # set score and random dropping
    score = 0
    y = 0
    x = random.randrange(1, dims[1]//2 - len(block[0]) - 1, 1)
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

        draw_Xs(screen, block, y, x)

        # moving with input of player
        if y < lines_Board - 2:
            check, block, x, y = move_X(block, x, y, input,
                                        board, lines_Board, dims)

        # board[y][x] = True

        # set score
        score = score + check_lines(board)

        # set up board
        draw_board(board, screen)

        # draw X
        draw_Xs(screen, block, y, x)

        # check end game
        if check or y >= lines_Board - len(block):
            for i in range(len(block)):
                for j in range(len(block[i])):
                    if block[i][j]:
                        board[y + i][x + j] = True
            game_over = is_game_over(board, y, x)
            index_list.append([y, x])
            x = random.randrange(1, dims[1]//2 - len(block[0]) - 1, 1)
            y = 0
            block = build_block()
        screen.addstr(dims[0]//2, dims[1]//2 + dims[1]//4 - 4,
                      "SCORE: %s" % score, curses.A_BOLD)
        screen.timeout(200)

    # throw message
    screen.clear()
    screen.addstr(2, 1, 'GAME OVER', curses.A_BOLD)
    screen.refresh()
    time.sleep(5)
    curses.endwin()


if __name__ == "__main__":
    playing_game()
