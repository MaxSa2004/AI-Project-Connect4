import math

#meta dados relativos ao jogo
class GameMeta:
    PLAYERS = {'none': 0, 'one': 1, 'two': 2}
    OUTCOMES = {'none': 0, 'one': 1, 'two': 2, 'draw': 3}
    INF = float('inf')
    ROWS = 6
    COLS = 7
    GAMEMODE = None

#valor C do UCB
class MCTSMeta:
    C = math.sqrt(2)
