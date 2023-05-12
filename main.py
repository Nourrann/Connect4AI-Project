# create a board and initialize it by zeros
RowsNum = 6
ColsNum = 7

def createBoard():
    board = []
    for i in range(RowsNum):
        row = [0] * ColsNum
        board.append(row)
    return board

# print the board
def printBoard(board):
    for row in board:
        print(row)

def dropPiece(board, row, col, piece):
    board[row][col] = piece

# #check if the cell in last row in a specif col is empty to drop a piece
# def isEmpty(board, col):
#     return board[RowsNum-1][col] == 0

# get the deepest available cell, return its row index
def getTheDeeppestEmptyRow(board, col):
    for i in range(RowsNum -1, -1, -1):
        if board[i][col] == 0:
            return i
    return -1



flag = True
board = createBoard()
tempBoard = board
turn = 1
while(flag):
    #printBoard(board)
    if turn == 1:
        col = int(input("Player 1, Enter the col: "))
        row = getTheDeeppestEmptyRow(tempBoard, col-1)
        piece = 1
        if row != -1:
            dropPiece(tempBoard, row, col-1, piece)
        else:
            print("Select another col!")
        board = tempBoard
        printBoard(board)
        print("------------")
        turn = 2
    elif turn == 2:
        col = int(input("Player 2, Enter the col: "))
        row = getTheDeeppestEmptyRow(tempBoard, col - 1)
        piece = 2
        if row != -1:
            dropPiece(tempBoard, row, col - 1, piece)
        else:
            print("Select another col!")
        board = tempBoard
        #print("board:", board[0][0])
        printBoard(board)
        print("------------")
        turn = 1


        #flag = False
    #if(turn == 0):




