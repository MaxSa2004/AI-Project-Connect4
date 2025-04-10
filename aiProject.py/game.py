from ConnectState import ConnectState
from mcts import MCTS
from meta import GameMeta

def playPvP():
    state = ConnectState()

    while not state.game_over():
        print("Current state:")
        state.print_board()

        p1Move = int(input("Enter a move: "))-1
        while p1Move not in state.get_legal_moves():
            print("Illegal move")
            p1Move = int(input("Enter a move: "))-1

        state.move(p1Move)
        state.print_board()

        if state.game_over():
            print("Player one ('X') won!")
            break

        p2Move = int(input("Enter a move: "))-1

        while p2Move not in state.get_legal_moves():
            print("Illegal move")
            p1Move = int(input("Enter a move: "))-1

        state.move(p2Move)
        state.print_board()

        if state.game_over():
            print("Player two ('O') won!")
            break

def playPvC():
    state = ConnectState()
    mcts = MCTS(state)
    changed_To_Attack = False # se o valor de C foi mudado ou não
    num_Plays = 0

    while not state.game_over():
        print("Current state:")
        state.print_board()

        user_move = int(input("Enter a move: "))-1
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))-1

        state.move(user_move)
        mcts.move(user_move)

        state.print_board()

        if state.game_over():
            print("Player one ('X') won!")
            break

        print("Thinking...")

        instaWin = mcts.check_instant_win(state)
        if instaWin != -1:
            print("MCTS chose move: ", instaWin+1)

            state.move(instaWin)
            mcts.move(instaWin)
        else:
            mcts.search(10)
            num_rollouts, run_time = mcts.statistics()
            print("Statistics: ", num_rollouts, "rollouts in", run_time, "seconds")
            move = mcts.best_move()

            print("MCTS chose move: ", move+1)

            state.move(move)
            mcts.move(move)

        if state.game_over():
            state.print_board()
            print("Player two ('O') won!")
            break

        if not changed_To_Attack:
            num_Plays += 2
            if num_Plays > 17:
                mcts.change_c_value()
                changed_To_Attack = True


'''
    Inicializador do modo de jogo pretendido:
    1. PvP
    2. PvC
    3. CvC
'''
if __name__ == "__main__":
    print("Welcome to Connect 4!\nPlease select one of the following game modes by selecting its corresponding number:\n1. Human vs. Human\n2. Human vs. Computer\n3. Computer vs. Computer")
    GameMeta.GAMEMODE = int(input("Select option:"))
    while 1 > GameMeta.GAMEMODE or GameMeta.GAMEMODE > 3:
        print("Invalid Gamemode")
        GameMeta.GAMEMODE = int(input("Select option:"))
    if GameMeta.GAMEMODE == 1:
        playPvP()
    elif GameMeta.GAMEMODE == 2:
        playPvC()
    elif GameMeta.GAMEMODE == 3:
        print("GAMEMODE 3 STILL TO BE DEVELOPED")
