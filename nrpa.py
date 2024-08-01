import random
from collections import defaultdict

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
        return self.make_move(*random.choice(empty_positions))

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


class NRPA:
    def __init__(self, level, iterations):
        self.level = level
        self.iterations = iterations

    def search(self, policy, node):
        return self.nrpa(self.level, policy, node)

    def nrpa(self, level, policy, node):
        if level == 0:
            reward, sequence = self.rollout(policy, node)
            return reward, sequence

        best_score = float('-inf')
        best_sequence = []

        for _ in range(self.iterations):
            new_policy = policy.copy()
            score, sequence = self.nrpa(level - 1, new_policy, node)
            if score > best_score:
                best_score = score
                best_sequence = sequence
                policy = self.adapt(policy, best_sequence)

        return best_score, best_sequence

    def rollout(self, policy, node):
        sequence = []
        while not node.is_terminal():
            moves = list(node.find_children())
            if not moves:
                break
            weights = [policy[move] for move in moves]
            total_weight = sum(weights)
            probabilities = [weight / total_weight for weight in weights]
            move = random.choices(moves, probabilities)[0]
            sequence.append(move)
            node = move

        return node.reward(), sequence

    def adapt(self, policy, sequence):
        learning_rate = 1.0
        for move in sequence:
            policy[move] += learning_rate
            learning_rate *= 0.9
        return policy

if __name__ == "__main__":
    board = new_hex_board(5)  # Use a smaller size for easier debugging
    policy = defaultdict(lambda: 1.0)
    nrpa = NRPA(level=3, iterations=10)

    while not board.is_terminal():
        _, sequence = nrpa.search(policy, board)
        if sequence:
            board = sequence[0]  # Take the first move of the best sequence
        print("Player move:")
        print(board.to_pretty_string())
        if board.is_terminal():
            print("Game Over. Winner:", "X" if board.winner else "O")
            break
