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

    # SQUARESIZE = 100

    # width = colNum * SQUARESIZE
    # height = (rowNum + 1) * SQUARESIZE

    # size = (width, height)

    # RADIUS = int(SQUARESIZE / 2 - 5)
        
    # screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    turn = random.randint(agent, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Ask for agent 1 Input
        if turn == agent:
            col, minimax_score = minimax(board, 2, True)

            if isValidCol(board, col):
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
            col, minimax_score = minimax(board, 5, True)

            if isValidCol(board, col):
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

        if turn == agent:
            col = random.randint(0, colNum-1)
            if isValidCol(board, col):
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
            col, minimax_score = minimax(board, 6, True)
            if isValidCol(board, col):
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
    


#GUI
root = Tk()
root.title("Connect-4")
root.minsize(400, 300)
label1 = Label(text= "Choose level of difficulty:", font=("Calibri bold", "15"))
label1.pack()
button3 = Button(text= "Difficult")
border = LabelFrame(root, bd = 6, bg = "Dark Green")
border.pack(pady = 10)
button1 = Button(border, text= "Easy", font=("Calibri bold", "10"), width = 30, bg = "#6CD400", fg = "black", command= runEasy)
button1.grid(padx=(0,0), pady=(200,0))
button2 = Button(border, text= "Regular", font=("Calibri bold", "10"), width = 30, bg = "#6CD400", fg = "black", command= runRegular)
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
    for i in range(0, rowNum-1, +1):
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
            if board[i][j] == mark and board[i][j+1] == mark and board[i][j+2] == mark and board[i][j+3] == mark:
                return True
    # Check vertical winning
    for i in range(rowNum - 3):
        for j in range(colNum):
            if board[i][j] == mark and board[i+1][j] == mark and board[i+2][j] == mark and board[i+3][j] == mark:
                return True
    # Check negative diagonal winning
    for i in range(rowNum - 3):
        for j in range(colNum - 3):
            if board[i][j] == mark and board[i+1][j+1] == mark and board[i+2][j+2] == mark and board[i+3][j+3] == mark:
                return True
    # Check positive diagonal winning
    for i in range(rowNum - 3):
        for j in range(3, colNum):
            if board[i][j] == mark and board[i+1][j-1] == mark and board[i+2][j-2] == mark and board[i+3][j-3] == mark:
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

    if window.count(AImark) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


# el ragel
def score_position(board, mark):
    score = 0

    ## Score center column
    # center_array = [int(i) for i in list(board[:, colNum // 2])]

    center_array = []
    for i in list(board[:, colNum//2]):
        center_array.append(int(i))

    score += center_array.count(mark) * 3


    ## Score Horizontal
    for r in range(rowNum):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(colNum - 3):
            window = row_array[c : c + windowSize]
            score += calculateScore(window, mark)

    ## Score Vertical
    for c in range(colNum):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(rowNum - 3):
            window = col_array[r : r + windowSize]
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


################################################################################################33
# def score_position(board, mark):
#     score = 0
#     center_col = colNum // 2
#     # Score center column
#     center_count = np.count_nonzero(board[:, center_col] == mark)
#     score += center_count * 3
#     # Score horizontal windows
#     for r in range(rowNum):
#         for c in range(colNum - windowSize + 1):
#             window = board[r, c : c + windowSize]
#             score += calculateScore(window, mark)
#     # Score vertical windows
#     for c in range(colNum):
#         for r in range(rowNum - windowSize + 1):
#             window = board[r : r + windowSize, c]
#             score += calculateScore(window, mark)
#     # Score positive slope diagonal windows
#     for r in range(rowNum - windowSize + 1):
#         for c in range(colNum - windowSize + 1):
#             window = board[r : r + windowSize, c : c + windowSize]
#             score += calculateScore(window.diagonal(), mark)
#             score += calculateScore(np.fliplr(window).diagonal(), mark)
#     return score


# Bta3tnaaaaaa
# def score_position(board, mark):
#     score = 0
#     ai_piece = agentmark if mark == AImark else AImark

#     # Score center column
#     center_count = sum([1 for i in range(rowNum) if board[i][colNum//2] == mark])
#     score += center_count * 3

#     # Score horizontal
#     for r in range(rowNum):
#         for c in range(colNum - 3):
#             window = board[r][c:c+windowSize]
#             score += calculateScore(window, mark)

#     # Score vertical
#     for c in range(colNum):
#         for r in range(rowNum - 3):
#             window = [board[r+i][c] for i in range(windowSize)]
#             score += calculateScore(window, mark)

#     # Score positive-sloped diagonal
#     for r in range(rowNum - 3):
#         for c in range(colNum - 3):
#             window = [board[r+i][c+i] for i in range(windowSize)]
#             score += calculateScore(window, mark)

#     # Score negative-sloped diagonal
#     for r in range(rowNum - 3):
#         for c in range(colNum - 3):
#             window = [board[r+3-i][c+i] for i in range(windowSize)]
#             score += calculateScore(window, mark)

#     # Subtract points for opponent's positions
#     for r in range(rowNum):
#         for c in range(colNum):
#             if board[r][c] == opp_piece:
#                 # Penalize for adjacent opponent pieces
#                 if c > 0 and board[r][c-1] == opp_piece:
#                     score -= 2
#                 if c < colNum-1 and board[r][c+1] == opp_piece:
#                     score -= 2
#                 if r > 0 and board[r-1][c] == opp_piece:
#                     score -= 2
#                 if r < rowNum-1 and board[r+1][c] == opp_piece:
#                     score -= 2

#                 # Penalize for opponent pieces on diagonal
#                 if r > 0 and c > 0 and board[r-1][c-1] == opp_piece:
#                     score -= 1
#                 if r < rowNum-1 and c > 0 and board[r+1][c-1] == opp_piece:
#                     score -= 1
#                 if r > 0 and c < colNum-1 and board[r-1][c+1] == opp_piece:
#                     score -= 1
#                 if r < rowNum-1 and c < colNum-1 and board[r+1][c+1] == opp_piece:
#                     score -= 1

#     return score
# #############################################################################################3

def is_terminal_node(board):

        if(isWinning(board, agentmark)):
            return 'agent'
        elif(isWinning(board, AImark)):
            return 'ai'
        elif(not len(eachValidColumn(board))):
            return 'full'
        else:
            return 0


def eachValidColumn(board):
    valid_locations = []
    for col in range(colNum):
        if isValidCol(board, col):
            valid_locations.append(col)
    return valid_locations


def minimax(board, depth, maximizingPlayer):
    value=0
    if depth == 0 or is_terminal_node(board):
        if is_terminal_node(board) == 'agent':
            return None, 100000000000
        elif is_terminal_node(board) == 'ai':
            return None, -100000000000
        elif is_terminal_node(board) == 'full':
            return None, 0
        else:
            return None, score_position(board, AImark)

    # valid_locations = eachValidColumn(board)
    highestValue = 0

    if maximizingPlayer:
        highestValue = -math.inf
        bestColumn = random.choice(eachValidColumn(board))

        for col in eachValidColumn(board):
            row = findDeepestRow(board, col)
            tempboard = board.copy()
            placeTiles(tempboard, row, col, AImark)
            value = minimax(tempboard, depth-1, False)[1]

            if highestValue < value:
                highestValue = value
                bestColumn = col

        return bestColumn, value

    else:
        lowestValue = math.inf
        bestColumn = random.choice(eachValidColumn(board))

        for col in eachValidColumn(board):
            row = findDeepestRow(board, col)
            tempboard = board.copy()
            placeTiles(tempboard, row, col, agentmark)
            value = minimax(tempboard, depth-1, True)[1]

            if value < lowestValue:
                lowestValue = value
                bestColumn = col

        return bestColumn, value


def pick_best_move(board, mark):
    valid_locations = eachValidColumn(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = findDeepestRow(board, col)
        temp_board = board.copy()
        placeTiles(temp_board, row, col, mark)
        score = score_position(temp_board, mark)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


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
