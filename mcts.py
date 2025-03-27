# Class for MCTS implementation
# Connect 4 project 24/25 - Maximiliano Sá, Orlando Soares, Rui Rua

grid = []

class mcts():
    def __init__(self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        #self.parent_action = parent_action
        self.children = []
        self.n = 0 # num visits
        self.wins = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()

    def untried_actions(self):
        self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    def validPos(self, col):
        return not grid[0][col] == 'O' or grid[0][col] == 'X'

    def get_legal_actions(self):
        res = []
        for i in range(1,8):
            if self.validPos(i):
                res.append(i)
        return res
    
