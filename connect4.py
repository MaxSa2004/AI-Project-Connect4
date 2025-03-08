# GLOBAL VARIABLES
grid = [['-' for _ in range(7)] for _ in range(6)]
xToPlay = True      # True if turn of X and False if turn of O
gameOver = False



def print_grid():
    print("  0123456")
    for i in range(6):
        print(str(i) + " " + ''.join(grid[i]))

def gameHandler(gameMode):
    if gameMode == 1:
        mode1()
    elif gameMode == 2:
        print()
    elif gameMode == 3:
        print()

# to complete
def mode1():
    while not gameOver:
        coord = 0
        if xToPlay:
            print_grid()
            coord = int(input("It is now X's turn.\nMake a move by choosing your coordinates to play:"))
            print()
        else:
            print_grid()
            coord = int(input("It is now O's turn.\nMake a move by choosing your coordinates to play:"))
            print()



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
