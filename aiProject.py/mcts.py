import random
import time
import math
from copy import deepcopy

from ConnectState import ConnectState
from meta import GameMeta, MCTSMeta


class Node:
    '''
        construtor da classe Node que guarda valores como o numero de visitas ao Nó, 
        número de vitórias, os seus filhos, o seu pai
    '''
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}
        self.outcome = GameMeta.PLAYERS['none']

    #adiciona os filhos ao dicionário do "children" do pai
    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child

    #calcular UCB do nó
    def value(self, c: float = MCTSMeta.C):
        if self.N == 0:
            return 0 if c == 0 else GameMeta.INF
        else:
            return self.Q / self.N + c * math.sqrt(math.log(self.parent.N) / self.N)


class MCTS:

    #Construtor da classe MCTS que guarda algumas estatísticas e é o ponto inicial do algoritmo
    def __init__(self, state=ConnectState()):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    #escolhe o próximo nó/estado a ser explorado
    def select_node(self) -> tuple:
        node = self.root
        state = deepcopy(self.root_state)

        #escolhe o nó filho com maior UCB (se o pai já tiver sido expandido)
        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.value()).value()
            max_nodes = [n for n in children if n.value() == max_value]

            node = random.choice(max_nodes)
            state.move(node.move)

            if node.N == 0:
                return node, state
            
        #escolhe aleatóriamente um nó filho para expandir
        if self.expand(node, state):
            node = random.choice(list(node.children.values()))
            state.move(node.move)

        return node, state

    #adiciona os estados seguintes como nós filho do estado atual
    def expand(self, parent: Node, state: ConnectState) -> bool:
        if state.game_over():
            return False

        children = [Node(move, parent) for move in state.get_legal_moves()]
        parent.add_children(children)

        return True

    #simula aleatóriamente um jogo e retorna o vencedor
    def roll_out(self, state: ConnectState) -> int:
        while not state.game_over():
            state.move(random.choice(state.get_legal_moves()))

        return state.get_outcome()

    #faz backtrack aos nós escolhidos na fase de rollout e dá update aos seus valores
    def back_propagate(self, node: Node, turn: int, outcome: int) -> None:
        # Para o jogador atual
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.N += 1
            node.Q += reward
            node = node.parent
            if outcome == GameMeta.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward

    #procura a melhor jogada por "time_limit" segundos
    def search(self, time_limit: int):
        start_time = time.process_time()

        num_rollouts = 0
        while time.process_time() - start_time < time_limit:
            node, state = self.select_node()
            outcome = self.roll_out(state)
            self.back_propagate(node, state.to_play, outcome)
            num_rollouts += 1

        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    #retorna a melhor jogada que o mcts encontrou
    def best_move(self):
        if self.root_state.game_over():
            return -1

        max_value = max(self.root.children.values(), key=lambda n: n.N).N
        max_nodes = [n for n in self.root.children.values() if n.N == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move

    #realiza (em definitivo) a melhor jogada que encontrou
    def move(self, move):
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return

        self.root_state.move(move)
        self.root = Node(None, None)

    #retorna estatísticas
    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time
