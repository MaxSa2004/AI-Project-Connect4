import json
from mcts import MCTS
from ConnectState import ConnectState
from copy import deepcopy
import os

def board_to_list(board):
    return [row[:] for row in board]

def generate_dataset_json(num_games, search_time, filename="mcts_dataset.json"):
    dataset = []

    # Load existing data if file exists
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                dataset = json.load(f)
            except json.JSONDecodeError:
                dataset = []

    for _ in range(num_games):
        state = ConnectState()
        mcts = MCTS(state)

        while not state.game_over():
            current_board = deepcopy(state.get_board())

            mcts.search(search_time)
            best_move = mcts.best_move()

            dataset.append({
                "state": board_to_list(current_board),
                "recommended_move": best_move
            })
            print(best_move)
            state.move(best_move)
            mcts.move(best_move)

    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)

    print(f"[✓] Dataset guardado em '{filename}' com {len(dataset)} pares.")



if __name__ == "__main__":
    print("Starting sim...")
    generate_dataset_json(1,5)