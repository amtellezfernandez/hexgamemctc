import random
import math
from collections import defaultdict
from random import choice

class MCTS:
    "Monte Carlo tree searcher with RAVE and additional strategies."

    def __init__(self, exploration_weight=1, rave_factor=500):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.RAVE_Q = defaultdict(int)  # total reward for RAVE
        self.RAVE_N = defaultdict(int)  # visit count for RAVE
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight
        self.rave_factor = rave_factor
        self.last_good_reply = {}

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            beta = self.rave_factor / (self.N[n] + self.RAVE_N[n] + self.rave_factor)
            q_value = self.Q[n] / self.N[n]
            rave_value = self.RAVE_Q[n] / self.RAVE_N[n] if self.RAVE_N[n] > 0 else 0
            return (1 - beta) * q_value + beta * rave_value

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward, actions = self._simulate(leaf)
        self._backpropagate(path, reward, actions)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        invert_reward = True
        actions = set()
        move_count = 0
        while True:
            if node.is_terminal():
                reward = node.reward() * (0.9 ** move_count)  # Discounted reward
                return (1 - reward if invert_reward else reward), actions
            action = node.find_random_child()
            actions.add(action.state)
            node = action
            invert_reward = not invert_reward
            move_count += 1


    def _backpropagate(self, path, reward, actions):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            for action in actions:
                self.RAVE_N[action] += 1
                self.RAVE_Q[action] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)

class HexBoard:
    def __init__(self, board, turn, winner, terminal):
        self.board = board
        self.turn = turn
        self.winner = winner
        self.terminal = terminal
        self.size = len(board)
        self.state = (tuple(tuple(row) for row in board), turn, winner, terminal)

    def find_children(self):
        if self.terminal:
            return set()
        return {self.make_move(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] is None}

    def find_random_child(self):
        if self.terminal:
            return None
        empty_positions = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] is None]
        return self.make_move(*choice(empty_positions))

    def reward(self):
        if not self.terminal:
            raise RuntimeError(f"reward called on nonterminal board {self}")
        if self.winner == self.turn:
            return 1
        if self.winner == (not self.turn):
            return 0
        if self.winner is None:
            return 0.5

    def is_terminal(self):
        return self.terminal

    def make_move(self, row, col):
        new_board = [list(r) for r in self.board]
        new_board[row][col] = self.turn
        next_turn = not self.turn
        winner = _find_winner(new_board, self.turn)
        is_terminal = winner is not None or all(new_board[r][c] is not None for r in range(self.size) for c in range(self.size))
        return HexBoard(new_board, next_turn, winner, is_terminal)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return isinstance(other, HexBoard) and self.state == other.state

    def to_pretty_string(self):
        to_char = lambda v: ("X" if v is True else ("O" if v is False else "."))
        rows = [
            " " * i + " ".join(to_char(cell) for cell in row) for i, row in enumerate(self.board)
        ]
        return "\n".join(rows) + "\n"

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def _find_winner(board, player):
    size = len(board)
    uf = UnionFind(size * size + 2)
    virtual_top = size * size
    virtual_bottom = size * size + 1

    def index(r, c):
        return r * size + c

    for r in range(size):
        for c in range(size):
            if board[r][c] == player:
                if r == 0 and player:  # Player X (True) starts at the top
                    uf.union(index(r, c), virtual_top)
                if r == size - 1 and player:  # Player X (True) ends at the bottom
                    uf.union(index(r, c), virtual_bottom)
                if c == 0 and not player:  # Player O (False) starts on the left
                    uf.union(index(r, c), virtual_top)
                if c == size - 1 and not player:  # Player O (False) ends on the right
                    uf.union(index(r, c), virtual_bottom)

                for dr, dc in [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == player:
                        uf.union(index(r, c), index(nr, nc))

    if uf.find(virtual_top) == uf.find(virtual_bottom):
        return player
    return None

def new_hex_board(size=11):
    return HexBoard(board=[[None for _ in range(size)] for _ in range(size)], turn=True, winner=None, terminal=False)



if __name__ == "__main__":
    board = new_hex_board(5)  # Use a smaller size for easier debugging
    tree = MCTS()

    while not board.is_terminal():
        # Player 1 (X) move
        for _ in range(50):
            tree.do_rollout(board)
        board = tree.choose(board)
        print("Player X move:")
        print(board.to_pretty_string())
        if board.is_terminal():
            print("Game Over. Winner:", "X" if board.winner else "O")
            break

        # Player 2 (O) move
        for _ in range(50):
            tree.do_rollout(board)
        board = tree.choose(board)
        print("Player O move:")
        print(board.to_pretty_string())
        if board.is_terminal():
            print("Game Over. Winner:", "X" if board.winner else "O")
            break
