# Class for MCTS implementation
# Connect 4 project 24/25 - Maximiliano Sá, Orlando Soares, Rui Rua

import mcts

grid = [['-' for _ in range(7)] for _ in range(6)]
xToPlay = True      # True if turn of X and False if turn of O
gameOver = False
winner = ""

def validPos(col):
    return not grid[0][col] == 'O' or grid[0][col] == 'X'

def print_grid():
    if not gameOver:
        print("")
        for i in range(6):
            print(''.join(grid[i]))
        print("1234567\n")

def gameHandler(gameMode):
    print_grid()
    if gameMode == 1:
        mode1()
    elif gameMode == 2:
        print()
    elif gameMode == 3:
        print()

# to complete
def mode1():
    while not gameOver:
        if xToPlay:
            column = int(input("It is now X's turn.\nChoose a column to play:"))
            placePiece(column-1)
        else:
            column = int(input("It is now O's turn.\nChoose a column to play:"))
            placePiece(column-1)

def placePiece(col):
    global xToPlay
    for line in range(5,-1,-1):
        if grid[line][col] == '-':
            if xToPlay:
                grid[line][col] = 'X'
            else:
                grid[line][col] = 'O'
            print_grid()
            verifyWin(line, col)
            xToPlay = not xToPlay
            return
    print("\n\n!!!ATTENTION: Column full, choose another column!!!\n\n")

def verifyWin(line, col):
    global gameOver
    if xToPlay:
        goal = 'X'
    else:
        goal = 'O'
    if verifyLine(line, goal) or verifyCol(col, goal) or verifyDiagonal1(line, col, goal) or verifyDiagonal2(line, col, goal):
        gameOver = True
        print(goal + " wins!!!!!!!")
    else:
        verifyDraw()

def verifyLine(line, goal):
    global winner
    cont = 0
    for i in range (7):
        if grid[line][i] == goal:
            cont += 1
            if cont == 4:
                winner = goal
                return True 
        else:
            cont = 0
    return False

def verifyCol(col, goal):
    global winner
    cont = 0
    for i in range (6):
        if grid[i][col] == goal:
            cont += 1
            if cont == 4:
                winner = goal
                return True 
        else:
            cont = 0
    return False

def verifyDiagonal1(line, col, goal):
    global winner
    cont = 1
    for i in range (1,4):
        if 5 >= line + i >= 0 and 6 >= col + i >= 0:
            if grid[line+i][col+i] == goal:
                cont += 1
                if cont == 4:
                    winner = goal
                    return True 
            else:
                break
        else:
            break

    for i in range (1,4):
        if 5 >= line - i >= 0 and 6 >= col - i >= 0:
            if grid[line-i][col-i] == goal:
                cont += 1
                if cont == 4:
                    winner = goal
                    return True 
            else:
                break 
        else:
            break

    return False

def verifyDiagonal2(line, col, goal):
    global winner
    cont = 1
    for i in range (1,4):
        if 5 >= line + i >= 0 and 6 >= col - i >= 0:
            if grid[line+i][col-i] == goal:
                cont += 1
                if cont == 4:
                    winner = goal
                    return True 
            else:
                break
        else:
            break

    for i in range (1,4):
        if 5 >= line - i >= 0 and 6 >= col + i >= 0:
            if grid[line-i][col+i] == goal:
                cont += 1
                if cont == 4:
                    winner = goal
                    return True 
            else:
                break 
        else:
            break

    return False

def verifyDraw():
    global gameOver
    for i in range (7):
        if grid[0][i] == '-':
            return
    gameOver = True
    print("Grid FULL. Draw!!")


    


# Note: human is X and computer is O
def main():
    # note grid has to be 7 wide and 6 high
    print("Welcome to Connect 4!\nPlease select one of the following game modes by selecting its corresponding number:\n1. Human vs. Human\n2. Human vs. Computer\n3. Computer vs. Computer")
    gameMode = int(input("Mode: "))
    gameHandler(gameMode)

    # testing:
    '''
    print("\ngrid[5][2] = 'X'\n")
    grid[5][2] = 'X'
    print_grid()
    '''



if __name__ == "__main__":
    main()