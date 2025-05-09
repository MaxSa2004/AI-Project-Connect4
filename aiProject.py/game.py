from ConnectState import ConnectState
from mcts import MCTS
from meta import GameMeta
from tree import trainTree
import numpy as np
import random

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
            result = state.get_result()
            if result == GameMeta.OUTCOMES['one']:
                print("Player one ('X') won!")
            else:
                print("Draw!")
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
            result = state.get_result()
            if result == GameMeta.OUTCOMES['two']:
                print("Player two ('O') won!")
            else:
                print("Draw!")
            break


def playPvC1():
    state = ConnectState()
    mcts = MCTS(state)
    changed_To_Attack = False # se o valor de C foi mudado ou não
    num_Plays = 0

    while not state.game_over():
        print("Current state:")
        state.print_board()

        # --- Human Player Move ---
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

        # --- MCTS Move ---
        state.move(user_move)
        mcts.move(user_move)
        state.print_board()

        if state.game_over():
            result = state.get_result()
            if result == GameMeta.OUTCOMES['one']:
                print("Player one ('X') won!")
            else:
                print("Draw!")
            break

        print("Thinking...")

        mcts.search(10)
        num_rollouts, run_time = mcts.statistics()
        print(f"Statistics: {num_rollouts} rollouts in {run_time:.2f} seconds")
        move = mcts.best_move()
        state.move(move)
        mcts.move(move)

        
        if state.game_over():
            state.print_board()
            result = state.get_result()
            if result == GameMeta.OUTCOMES['two']:
                print("Player two ('O') won!")
            else:
                print("Draw!")
            break

        if not changed_To_Attack:
            num_Plays += 2
            if num_Plays > 17:
                mcts.change_c_value()
                changed_To_Attack = True

def playPvC2():
    state = ConnectState()
    tree = trainTree()

    while not state.game_over():
        print("Current state:")
        state.print_board()

        # --- Human Player Move ---
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
        state.print_board()

        if state.game_over():
            result = state.get_result()
            if result == GameMeta.OUTCOMES['one']:
                print("Player one ('X') won!")
            else:
                print("Draw!")
            break

        # --- Decision Tree Move ---
        new_state = np.array(state.get_board()).flatten()
        predicted_move = tree.predict(np.array([new_state]))[0]
        legal_moves = state.get_legal_moves()

        if predicted_move not in legal_moves:
            state.move(legal_moves[random.randint(0, len(legal_moves)-1)])
        else:
            state.move(predicted_move)

        print("Tree chose to play in column: " + str(predicted_move+1))

        if state.game_over():
            state.print_board()
            result = state.get_result()
            if result == GameMeta.OUTCOMES['two']:
                print("Player two ('O') won!")
            else:
                print("Draw!")
            break

def playCvC():
    state = ConnectState()
    tree = trainTree()
    mcts = MCTS(state)
    changed_To_Attack = False
    num_Plays = 0
    print("Current state:")
    state.print_board()

    while not state.game_over():
        # --- MCTS turn ---
        print("Thinking (MCTS)...")
        mcts.search(10)
        num_rollouts, run_time = mcts.statistics()
        print(f"Statistics: {num_rollouts} rollouts in {run_time:.2f} seconds")

        mcts_move = mcts.best_move()
        state.move(mcts_move)
        mcts.move(mcts_move)

        print("MCTS chose column:", mcts_move + 1)
        state.print_board()

        if state.game_over():
            result = state.get_result()
            if result == GameMeta.OUTCOMES['one']:
                print("MCTS ('X') won!")
            else:
                print("Draw!")
            break

        # --- Tree turn ---
        new_state = np.array(state.get_board()).flatten()
        predicted_move = tree.predict(np.array([new_state]))[0]

        legal_moves = state.get_legal_moves()
        if predicted_move not in legal_moves:
            # fallback to random legal move
            predicted_move = random.choice(legal_moves)

        state.move(predicted_move)
        mcts.move(predicted_move)

        print("Tree chose column:", predicted_move + 1)
        state.print_board()

        if state.game_over():
            result = state.get_result()
            if result == GameMeta.OUTCOMES['two']:
                print("Tree ('O') won!")
            else:
                print("Draw!")
            break

        # Optionally adjust MCTS’s C parameter after a number of full turns
        if not changed_To_Attack:
            num_Plays += 2
            if num_Plays > 17:
                mcts.change_c_value()
                changed_To_Attack = True
    


'''
    Inicializador do modo de jogo pretendido:
    1. PvP
    2. PvC (mcts)
    3. PvC (tree)
    4. CvC
'''
if __name__ == "__main__":
    print("Welcome to Connect 4!\nPlease select one of the following game modes by selecting its corresponding number:\n1. Human vs. Human\n2. Human vs. Computer(MCTS)\n3. Human vs. Computer(Tree)\n4. Computer(MCTS) vs. Computer(Tree)")
    GameMeta.GAMEMODE = int(input("Select option:"))
    while 1 > GameMeta.GAMEMODE or GameMeta.GAMEMODE > 4:
        print("Invalid Gamemode")
        GameMeta.GAMEMODE = int(input("Select option:"))
    if GameMeta.GAMEMODE == 1:
        playPvP()
    elif GameMeta.GAMEMODE == 2:
        playPvC1()
    elif GameMeta.GAMEMODE == 3:
        playPvC2()
    else:
        playCvC()
