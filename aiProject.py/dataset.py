import json
from mcts import MCTS
from ConnectState import ConnectState
from copy import deepcopy
import os

def board_to_list(board):
    return [row[:] for row in board]

def get_player_symbol(player_num):
    return 'X' if player_num == 1 else 'O'

def generate_dataset_json(num_games, search_time, filename="mcts_dataset.json"):
    dataset = []

    # Carrega o dataset existente (se houver)
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                dataset = json.load(f)
            except json.JSONDecodeError:
                dataset = []

    for game_index in range(num_games):
        state = ConnectState()
        mcts = MCTS(state)
        move_count = 1
        changed_To_Attack = False # se o valor de C foi mudado ou não

        print(f"\n=== Início do Jogo {game_index + 1} ===\n")
        state.print_board()

        while not state.game_over():
            current_board = deepcopy(state.get_board())

            mcts.search(search_time)
            best_move = mcts.best_move()

            dataset.append({
                "state": board_to_list(current_board),
                "recommended_move": best_move
            })

            current_player = get_player_symbol(state.to_play)

            print(f"\n Jogada {move_count} | Jogador '{current_player}' joga na coluna {best_move + 1}")
            state.move(best_move)
            state.print_board()

            mcts.move(best_move)
            move_count += 1

            if not changed_To_Attack:
                if move_count > 17:
                    mcts.change_c_value()
                    changed_To_Attack = True

    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"\n[✓] Dataset guardado em '{filename}' com {len(dataset)} pares totais.")

if __name__ == "__main__":
    print("Starting sim...")
    generate_dataset_json(20, 10)
