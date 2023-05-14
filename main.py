import math
import random

RowsNum = 6
ColsNum = 7
Empty = 0
PLAYER = 1
OPPONENT = 2  # AI

def createBoard():
    board = []
    for i in range(RowsNum):
        row = [Empty] * ColsNum
        board.append(row)
    return board

def printBoard(board):
    for row in board:
        print(row)

def dropPiece(board, row, col, piece):
    board[row][col] = piece

def isEmpty(board, col):
    return board[RowsNum-1][col] == Empty

def getTheDeeppestEmptyRow(board, col):
    for i in range(RowsNum - 1, -1, -1):
        if board[i][col] == Empty:
            return i
    return -1

def get_valid_locations(board):
    valid_locations = []
    for col in range(ColsNum):
        if isEmpty(board, col):
            valid_locations.append(col)
    return valid_locations

def playerScore(board, piece):
    # Check horizontal winning
    for i in range(RowsNum):
        for j in range(ColsNum - 3):
            if board[i][j] == piece and board[i][j+1] == piece and board[i][j+2] == piece and board[i][j+3] == piece:
                return True
    # Check vertical winning
    for i in range(RowsNum - 3):
        for j in range(ColsNum):
            if board[i][j] == piece and board[i+1][j] == piece and board[i+2][j] == piece and board[i+3][j] == piece:
                return True
    # Check negative diagonal winning
    for i in range(RowsNum - 3):
        for j in range(ColsNum - 3):
            if board[i][j] == piece and board[i+1][j+1] == piece and board[i+2][j+2] == piece and board[i+3][j+3] == piece:
                return True
    # Check positive diagonal winning
    for i in range(RowsNum - 3):
        for j in range(3, ColsNum):
            if board[i][j] == piece and board[i+1][j-1] == piece and board[i+2][j-2] == piece and board[i+3][j-3] == piece:
                return True
    return False

def calculateScore(window, piece):
    aiPiece = OPPONENT
    opponentPlayer = PLAYER

    if piece == PLAYER:
        opponentPlayer = OPPONENT
    if window.count(piece) == 4:
        return 1000
    elif window.count(piece) == 3 and window.count(Empty) == 1:
        return 5
    elif window.count(piece) == 2 and window.count(Empty) == 2:
        return 2
    elif window.count(opponentPlayer) == 3 and window.count(Empty) == 1:
        return -4
    else:
        return 0
    

def score_position(board, piece):
    score = 0
    opp_piece = PLAYER if piece == OPPONENT else OPPONENT
    
    # Score center column
    center_count = sum([1 for i in range(RowsNum) if board[i][ColsNum//2] == piece])
    score += center_count * 3
    
    # Score horizontal
    for r in range(RowsNum):
        for c in range(ColsNum - 3):
            window = board[r][c:c+4]
            score += calculateScore(window, piece)
    
    # Score vertical
    for c in range(ColsNum):
        for r in range(RowsNum - 3):
            window = [board[r+i][c] for i in range(4)]
            score += calculateScore(window, piece)
    
    # Score positive-sloped diagonal
    for r in range(RowsNum - 3):
        for c in range(ColsNum - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += calculateScore(window, piece)
    
    # Score negative-sloped diagonal
    for r in range(RowsNum - 3):
        for c in range(ColsNum - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += calculateScore(window, piece)
    
    # Subtract points for opponent's positions
    for r in range(RowsNum):
        for c in range(ColsNum):
            if board[r][c] == opp_piece:
                # Penalize for adjacent opponent pieces
                if c > 0 and board[r][c-1] == opp_piece:
                    score -= 2
                if c < ColsNum-1 and board[r][c+1] == opp_piece:
                    score -= 2
                if r > 0 and board[r-1][c] == opp_piece:
                    score -= 2
                if r < RowsNum-1 and board[r+1][c] == opp_piece:
                    score -= 2
                
                # Penalize for opponent pieces on diagonal
                if r > 0 and c > 0 and board[r-1][c-1] == opp_piece:
                    score -= 1
                if r < RowsNum-1 and c > 0 and board[r+1][c-1] == opp_piece:
                    score -= 1
                if r > 0 and c < ColsNum-1 and board[r-1][c+1] == opp_piece:
                    score -= 1
                if r < RowsNum-1 and c < ColsNum-1 and board[r+1][c+1] == opp_piece:
                    score -= 1
    
    return score

def isTerminalNode(board):
    arr_length = len(get_valid_locations(board))
    if playerScore(board, PLAYER) or playerScore(board, OPPONENT) or arr_length == 0:
        return True
    else:
        return False

def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = isTerminalNode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if playerScore(board, OPPONENT):
                return None, 100000000000000

            elif playerScore(board, PLAYER) :
                return None, -10000000000000
            else: # Game is over, no more valid moves
                return None, 0
        else: # Depth is zero
            return None, score_position(board, OPPONENT)
        
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getTheDeeppestEmptyRow(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, OPPONENT)
            new_score = minimax(b_copy, depth-1, False)[1] 
            if new_score > value:
                value = new_score
                column = col
        return column, value
    
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getTheDeeppestEmptyRow(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, PLAYER)
            new_score = minimax(b_copy, depth-1, True)[1]

            if new_score < value:
                value = new_score
                column = col
        return column, value

flag = True
board = createBoard()
tempBoard = board
turn = 1
while(flag):
    if turn == 1:
        col = int(input("Player 1, Enter the col: "))
        row = getTheDeeppestEmptyRow(tempBoard, col-1)
        piece = PLAYER
        if row != -1:
            dropPiece(tempBoard, row, col-1, piece)
            if playerScore(board, piece):
                print("Player 1 wins!!")
                flag = False
        else:
            print("Select another col!")
        board = tempBoard
        printBoard(board)
        print("------------")
        turn = 2
    elif turn == 2:
        col = minimax(board, 5, True)
        row = getTheDeeppestEmptyRow(tempBoard, col- 1)
        piece = OPPONENT
        if row != -1:
            dropPiece(tempBoard, row, col - 1, piece)
            if playerScore(board, piece):
                print("Player 2 wins!!")
                flag = False
        else:
            print("Select another col!")
        board = tempBoard
        printBoard(board)
        print("------------")
        turn = 1
    if flag == True and len(get_valid_locations(board)) == 0:
        print("No one wins!")
        flag = False