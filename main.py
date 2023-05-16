from tkinter import *
import numpy as np
import random
import pygame
import sys
import math

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

rowNum = 6
colNum = 7

agent = 0
AI = 1

EMPTY = 0
agentmark = 1
AImark = 2
maximizingPlayer = 1
minimizingPlayer = 0

windowSize = 4

SQUARESIZE = 100
width = colNum * SQUARESIZE
height = (rowNum + 1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)
screen = pygame.display.set_mode(size)


def runRegular():
    board = generateBoard()
    printBoard(board)
    game_over = False

    pygame.init()

    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(agent, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pygame.display.update()
        # Ask for agent 1 Input
        if turn == agent:
            col,scorer = minimax(board, 3, True)

            if isValidCol(board, col):
                pygame.time.wait(700)
                row = findDeepestRow(board, col)
                placeTiles(board, row, col, agentmark)

                if isWinning(board, agentmark):
                    label = myfont.render("agent 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

                printBoard(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        # Ask for agent 2 Input
        if turn == AI and not game_over:
            col,scorer = minimax(board, 5, True)

            if isValidCol(board, col):
                pygame.time.wait(700)
                row = findDeepestRow(board, col)
                placeTiles(board, row, col, AImark)

                if isWinning(board, AImark):
                    label = myfont.render("agent 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                printBoard(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)


def runEasy():
    board = generateBoard()
    printBoard(board)
    game_over = False

    pygame.init()
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(agent, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            pygame.display.update()
        if turn == agent:
            col = pick_best_move(board, agentmark)
            if isValidCol(board, col):
                pygame.time.wait(700)
                row = findDeepestRow(board, col)
                placeTiles(board, row, col, agentmark)

                if isWinning(board, agentmark):
                    label = myfont.render("agent 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn += 1
                turn = turn % 2

                printBoard(board)
                draw_board(board)

        # Ask for agent 2 Input
        if turn == AI and not game_over:
            col,scorer = minimax(board, 4, True)
            if isValidCol(board, col):
                pygame.time.wait(700)
                row = findDeepestRow(board, col)
                placeTiles(board, row, col, AImark)

                if isWinning(board, AImark):
                    label = myfont.render("agent 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                printBoard(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)


# GUI
root = Tk()
root.title("Connect-4")
root.minsize(400, 300)
label1 = Label(text="Choose level of difficulty:", font=("Calibri bold", "15"))
label1.pack()
button3 = Button(text="Difficult")
border = LabelFrame(root, bd=6, bg="Dark Green")
border.pack(pady=10)
button1 = Button(border, text="Easy", font=("Calibri bold", "10"), width=30, bg="#6CD400", fg="black", command=runEasy)
button1.grid(padx=(0, 0), pady=(200, 0))
button2 = Button(border, text="Regular", font=("Calibri bold", "10"), width=30, bg="#6CD400", fg="black",
                 command=runRegular)
button1.pack()
button2.pack()


def generateBoard():
    board = np.zeros((rowNum, colNum))
    return board


def placeTiles(board, row, col, mark):
    board[row][col] = mark


def isValidCol(board, col):
    return board[rowNum - 1][col] == 0


def findDeepestRow(board, col):
    for i in range(0, rowNum - 1, +1):
        if board[i][col] == EMPTY:
            return i
    return -1


def printBoard(board):
    for row in board:
        print(row)


def isWinning(board, mark):
    # Check horizontal winning
    for i in range(rowNum):
        for j in range(colNum - 3):
            if board[i][j] == mark and board[i][j + 1] == mark and board[i][j + 2] == mark and board[i][j + 3] == mark:
                return True
    # Check vertical winning
    for i in range(rowNum - 3):
        for j in range(colNum):
            if board[i][j] == mark and board[i + 1][j] == mark and board[i + 2][j] == mark and board[i + 3][j] == mark:
                return True
    # Check negative diagonal winning
    for i in range(rowNum - 3):
        for j in range(colNum - 3):
            if board[i][j] == mark and board[i + 1][j + 1] == mark and board[i + 2][j + 2] == mark and board[i + 3][
                j + 3] == mark:
                return True
    # Check positive diagonal winning
    for i in range(rowNum - 3):
        for j in range(3, colNum):
            if board[i][j] == mark and board[i + 1][j - 1] == mark and board[i + 2][j - 2] == mark and board[i + 3][
                j - 3] == mark:
                return True
    return False


def calculateScore(window, mark):
    score = 0
    ai_piece = agentmark
    if mark == agentmark:
        ai_piece = AImark

    if window.count(mark) == 4:
        score += 100
    elif window.count(mark) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(mark) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(ai_piece) == 3 and window.count(EMPTY) == 1:
        score -= 100
    elif window.count(ai_piece) == 2 and window.count(EMPTY) == 2:
        score -= 5
    return score


def score_position(board, mark):
    score = 0

    center_array = []
    for i in list(board[:, colNum // 2]):
        center_array.append(int(i))

    score += center_array.count(mark) * 3

    ## Score Horizontal
    for r in range(rowNum):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(colNum - 3):
            window = row_array[c: c + windowSize]
            score += calculateScore(window, mark)

    ## Score Vertical
    for c in range(colNum):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rowNum - 3):
            window = col_array[r: r + windowSize]
            score += calculateScore(window, mark)

    ## Score posiive sloped diagonal
    for r in range(rowNum - 3):
        for c in range(colNum - 3):
            window = [board[r + i][c + i] for i in range(windowSize)]
            score += calculateScore(window, mark)

    for r in range(rowNum - 3):
        for c in range(colNum - 3):
            window = [board[r + 3 - i][c + i] for i in range(windowSize)]
            score += calculateScore(window, mark)

    return score



def is_terminal_node(board):
    return isWinning(board, agentmark) or isWinning(board, AImark) or len(eachValidColumn(board)) == 0


def eachValidColumn(board):
    valid_locations = []
    for col in range(colNum):
        if isValidCol(board, col):
            valid_locations.append(col)
    return valid_locations


def getOpponent(player):
    if player == agent:
        return AI
    else:
        return agent


def minimax(board, depth, maximizingPlayer):
    validCols = eachValidColumn(board)
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board):
            if isWinning(board, AImark):
               return None, 100000000000000
            elif is_terminal_node(board) :
              if isWinning(board, agentmark):
               return None, -10000000000000
            else :
             return None, 0
        else:
            return None, score_position(board, AImark)

    if maximizingPlayer:
        bestScore = -math.inf
        colNum = random.choice(validCols)
        for col in validCols:
            row = findDeepestRow(board, col)
            tempBoard = board.copy()
            tempBoard[row][col] = AImark
            score = minimax(tempBoard, depth - 1, False)[1]
            if score > bestScore:
                bestScore = score
                colNum = col
        return colNum, bestScore
    else:
        bestScore = math.inf
        colNum = random.choice(validCols)
        for col in validCols:
            row = findDeepestRow(board, col)
            tempBoard = board.copy()
            tempBoard[row][col] = agentmark
            score = minimax(tempBoard, depth - 1, True)[1]
            if score < bestScore:
                bestScore = score
                colNum = col
        return colNum, bestScore


def draw_board(board):
    for c in range(colNum):
        for r in range(rowNum):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2),
                ),
                RADIUS,
            )

    for c in range(colNum):
        for r in range(rowNum):
            if board[r][c] == agentmark:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == AImark:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        height - int(r * SQUARESIZE + SQUARESIZE / 2),
                    ),
                    RADIUS,
                )
    pygame.display.update()


root.mainloop()