# hexgamemctc
Monte Carlo Search approach to HEX game
# Monte Carlo Tree Search (MCTS) and Variants

Monte Carlo Tree Search (MCTS) is a heuristic search algorithm used for decision-making processes, especially in game theory. It is widely applied in artificial intelligence for games like Go, Chess, and Tic-Tac-Toe. The algorithm builds a search tree incrementally and uses random simulations to estimate the value of each move.

## Algorithm Overview

MCTS consists of four main steps:

1. **Selection:** Starting from the root node, recursively select child nodes until a leaf node is reached. The selection of child nodes is guided by a policy, usually the Upper Confidence Bound for Trees (UCT) formula.
2. **Expansion:** If the leaf node is not terminal (i.e., it can have children), expand the tree by adding one or more child nodes.
3. **Simulation (Rollout):** Perform a random simulation from the expanded node to a terminal state of the game. The result of this simulation (win, loss, or draw) is recorded.
4. **Backpropagation:** Propagate the simulation result back through the tree, updating the statistics (total reward and visit count) of each node along the path.

### Upper Confidence Bound for Trees (UCT) Formula

The UCT formula is used in the selection step to balance exploration and exploitation. The goal is to choose nodes that have high potential for good outcomes (exploitation) while also exploring less-visited nodes to discover their potential (exploration).

\[ UCT(n) = \frac{Q(n)}{N(n)} + c \sqrt{\frac{\log N(p)}{N(n)}} \]

where:
- \( Q(n) \) is the total reward of node \( n \).
- \( N(n) \) is the visit count of node \( n \).
- \( N(p) \) is the visit count of the parent node \( p \).
- \( c \) is the exploration parameter (e.g., \( c = \sqrt{2} \)).

## Exploration vs. Exploitation

The UCT formula consists of two terms:

1. **Exploitation:** \(\frac{Q(n)}{N(n)}\) represents the average reward of node \( n \). Nodes with higher average rewards are preferred.
2. **Exploration:** \( c \sqrt{\frac{\log N(p)}{N(n)}}\) encourages the algorithm to explore less-visited nodes.

## Technical Implementation

The `MCTS` class maintains:

- `Q`: A defaultdict to store the total reward of each node.
- `N`: A defaultdict to store the visit count of each node.
- `children`: A dictionary to store the children of each node.
- `exploration_weight`: The exploration parameter \( c \).

The `choose` method uses the UCT formula to select the best child node, while the `do_rollout` method performs the selection, expansion, simulation, and backpropagation steps to improve the tree iteratively.


### MCTS for Hex

The `HexBoard` class represents the game state for Hex. It includes methods for finding children, making random moves, checking terminal states, and calculating rewards. The player X wins if they connect from top to bottom, and player O wins if they connect right to left. To identify the winner, a Union-Find (or Disjoint Set Union, DSU) data structure is used to determine connectivity in the `HexBoard`.

#### Union-Find Data Structure

- `find(u)`: Determines the representative (or root) of the set containing element \( u \). This operation checks if two elements are in the same set.
- `union(u, v)`: Merges the sets containing elements \( u \) and \( v \).

### Example Games Using MCTS with RAVE and NRPA

MCTS can be enhanced using various strategies:

#### MCTS with RAVE

The Rapid Action Value Estimation (RAVE) algorithm helps warm up the tree faster by sharing information among nodes that share the same move, leading to faster convergence.

The RAVE-adjusted score is calculated as follows:

\[ \text{score}(n) = (1 - \beta) \frac{Q(n)}{N(n)} + \beta \frac{RAVE_Q(n)}{RAVE_N(n)} \]

where

\[ \beta = \frac{\text{rave\_factor}}{N(n) + RAVE_N(n) + \text{rave\_factor}} \]

#### Nested Rollout Policy Adaptation (NRPA)

NRPA searches for the best sequence of moves by performing rollouts and adapting the policy based on the observed rewards.

- **NRPA(level, policy, node):** Recursively searches for the best sequence of moves.
- **rollout(policy, node):** Simulates a game from the given node following the provided policy until the game is terminal.
- **adapt(policy, sequence):** Adjusts the policy based on the sequence of moves from a successful rollout.

### NRPA Example Game

An NRPA instance is created with a search depth of 3 and 10 iterations for policy adaptation, demonstrating a self-play game with player moves until the game is terminal.


## Conclusion

MCTS and its variants, such as RAVE and NRPA, are powerful algorithms for decision-making in complex games. They provide a framework for balancing exploration and exploitation, adapting strategies dynamically, and efficiently searching through large decision spaces.
