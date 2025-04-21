from ConnectState import ConnectState
from mcts import MCTS
from meta import GameMeta

def playPvP():
    state = ConnectState()

    while not state.game_over():
        print("Current state:")
        state.print_board()

        # --- Player 1 Move ---
        while True:
            p1_input = input("Player 1 ('X') enter a move: ")
            if not p1_input.strip():
                print("You need to enter a move.")
                continue
            try:
                p1Move = int(p1_input) - 1
            except ValueError:
                print("That's not a valid number. Try again.")
                continue

            if p1Move not in state.get_legal_moves():
                print("Illegal move")
                continue
            break

        state.move(p1Move)
        state.print_board()

        if state.game_over():
            print("Player one ('X') won!")
            break

        # --- Player 2 Move ---
        while True:
            p2_input = input("Player 2 ('O') enter a move: ")
            if not p2_input.strip():
                print("You need to enter a move.")
                continue
            try:
                p2Move = int(p2_input) - 1
            except ValueError:
                print("That's not a valid number. Try again.")
                continue

            if p2Move not in state.get_legal_moves():
                print("Illegal move")
                continue
            break

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

        while True:
            user_input = input("Enter a move: ")
            # Check if input is blank or not a number
            if not user_input.strip():
                print("You need to enter a move.")
                continue
            try:
                user_move = int(user_input) - 1
            except ValueError:
                print("That's not a valid number. Try again.")
                continue
            if user_move not in state.get_legal_moves():
                print("Illegal move")
                continue
            break  # valid input and legal move

        state.move(user_move)
        mcts.move(user_move)

        state.print_board()

        if state.game_over():
            print("Player one ('X') won!")
            break

        print("Thinking...")

        compIsWinner = False
        instaWin = mcts.check_instant_win(state) # check if can win in 1 move
        if instaWin != -1:
            compIsWinner = True
            print("MCTS chose move: ", instaWin+1)
            state.move(instaWin)
            mcts.move(instaWin)
        else:
            oneMoveOnly = mcts.check_one_move_available(state) # check if only exists 1 move (no need to think if only 1 option)
            if oneMoveOnly != -1:
                print("MCTS chose move: ", oneMoveOnly+1)
                state.move(oneMoveOnly)
                mcts.move(oneMoveOnly)
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
            if compIsWinner:
                print("Player two ('O') won!")
            else:
                print("Draw!")
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
