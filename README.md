# hexgamemctc
Monte Carlo Search approach to HEX game


\section{Monte Carlo Tree Search (MCTS)}

Monte Carlo Tree Search (MCTS) is a heuristic search algorithm used for decision-making processes, especially in game theory. It is widely used in artificial intelligence for games like Go, Chess, and Tic-Tac-Toe. The algorithm builds a search tree incrementally and uses random simulations to estimate the value of each move. MCTS consists of four main steps:

\subsubsection*{1. Selection}
Starting from the root node, recursively select child nodes until a leaf node is reached. The selection of child nodes is guided by a policy, usually the Upper Confidence Bound for Trees (UCT) formula.

\subsubsection*{2. Expansion}
If the leaf node is not terminal (i.e., it can have children), expand the tree by adding one or more child nodes.

\subsubsection*{3. Simulation (Rollout)}
Perform a random simulation from the expanded node to a terminal state of the game. The result of this simulation (win, loss, or draw) is recorded.

\subsubsection*{4. Backpropagation}
Propagate the simulation result back through the tree, updating the statistics (total reward and visit count) of each node along the path.

\subsubsection*{Upper Confidence Bound for Trees (UCT) Formula}

The UCT formula is used in the selection step to balance exploration and exploitation. The goal is to choose nodes that have high potential for good outcomes (exploitation) while also exploring less-visited nodes to discover their potential (exploration).

The UCT formula is given by:

\[
UCT(n) = \frac{Q(n)}{N(n)} + c \sqrt{\frac{\log N(p)}{N(n)}}
\]

where:
\begin{itemize}
    \item $Q(n)$ is the total reward of node $n$.
    \item $N(n)$ is the visit count of node $n$.
    \item $N(p)$ is the visit count of the parent node $p$.
    \item $c$ is the exploration parameter (exploration weight), which balances exploration and exploitation. A typical value is $c = \sqrt{2}$.
\end{itemize}

\subsection*{Exploration vs. Exploitation}

The UCT formula consists of two terms:
\begin{enumerate}
    \item \(\frac{Q(n)}{N(n)}\): This is the exploitation term, representing the average reward of node $n$. Nodes with higher average rewards are preferred.
    \item \(c \sqrt{\frac{\log N(p)}{N(n)}}\): This is the exploration term. Nodes with fewer visits $N(n)$ will have a higher exploration value, encouraging the algorithm to explore less-visited nodes.
\end{enumerate}

The balance between these two terms ensures that the MCTS algorithm explores a diverse range of moves while focusing on those that have shown promise in previous simulations.


\subsubsection*{Logarithmic Term}
The logarithmic term $\log N(p)$ grows slowly, ensuring that as the number of visits to the parent node $p$ increases, the influence of the exploration term decreases. This ensures that the algorithm does not over-explore nodes that have already been sufficiently explored.

\subsubsection*{Square Root Term}
The square root term $\sqrt{\frac{1}{N(n)}}$ ensures that the exploration value decreases as the visit count $N(n)$ increases. This encourages the algorithm to explore new nodes initially and gradually focus on exploitation as more information is gathered.

\subsubsection*{Technical Implementation}

In the implementation, the MCTS class maintains the following:
\begin{itemize}
    \item \texttt{Q}: A defaultdict to store the total reward of each node.
    \item \texttt{N}: A defaultdict to store the visit count of each node.
    \item \texttt{children}: A dictionary to store the children of each node.
    \item \texttt{exploration\_weight}: The exploration parameter $c$.
\end{itemize}

The \texttt{choose} method uses the UCT formula to select the best child node, while the \texttt{do\_rollout} method performs the selection, expansion, simulation, and backpropagation steps to improve the tree iteratively.

\subsection{MCTS for tictactoe:}
Monte Carlo Tree Search (MCTS) algorithm for playing a game, specifically Tic-Tac-Toe.

\begin{verbatim}
  1 2 3
1      
2      
3      

  1 2 3
1      
2      
3     X

  1 2 3
1      
2      
3   O X

  1 2 3
1      
2     X
3   O X

  1 2 3
1     O
2     X
3   O X

  1 2 3
1     O
2   X X
3   O X

  1 2 3
1 O   O
2   X X
3   O X

  1 2 3
1 O   O
2 X X X
3   O X
\end{verbatim}

\subsection{MCTS for 4 in a row:}
\begin{verbatim}
                 
             
             
             
             
          X  

             
             
             
             
             
      O   X  

             
             
             
             
             
X     O   X  

             
             
             
             
      O      
X     O   X  

             
             
             
      X      
      O      
X     O   X  

             
             
             
      X      
      O      
X   O O   X  

             
             
             
      X      
X     O      
X   O O   X  

             
             
             
O     X      
X     O      
X   O O   X  

             
             
             
O     X      
X     O      
X X O O   X  

             
             
             
O     X      
X O   O      
X X O O   X  

             
             
      X      
O     X      
X O   O      
X X O O   X  

             
      O      
      X      
O     X      
X O   O      
X X O O   X  

             
      O      
X     X      
O     X      
X O   O      
X X O O   X  

             
      O      
X     X      
O     X      
X O O O      
X X O O   X  

             
      O      
X     X      
O   X X      
X O O O      
X X O O   X  

             
O     O      
X     X      
O   X X      
X O O O      
X X O O   X  

             
O     O      
X   X X      
O   X X      
X O O O      
X X O O   X  

             
O   O O      
X   X X      
O   X X      
X O O O      
X X O O   X  

X            
O   O O      
X   X X      
O   X X      
X O O O      
X X O O   X  

X            
O   O O      
X   X X      
O   X X      
X O O O      
X X O O   X O

X     X      
O   O O      
X   X X      
O   X X      
X O O O      
X X O O   X O

X   O X      
O   O O      
X   X X      
O   X X      
X O O O      
X X O O   X O

X   O X      
O   O O      
X   X X      
O X X X      
X O O O      
X X O O   X O

X   O X      
O   O O      
X O X X      
O X X X      
X O O O      
X X O O   X O

X   O X      
O X O O      
X O X X      
O X X X      
X O O O      
X X O O   X O

Game Over
\end{verbatim}

\section{Monte Carlo Search for HEX:}
The HexBoard class represents the game state for Hex. It includes methods for finding children, making random moves, checking terminal states, and calculating rewards.

The player X wins if he connects from top to bottom and player O wins if he connects right to left. To identify this situation i use the UnionFind class to determine the connectivity in the HexBoard so that i can identify the winner. The UnionFind (or Disjoint Set Union, DSU) data structure supports two primary operations:

\begin{itemize}
    \item \texttt{find(u)}: Determines the representative (or root) of the set containing element $u$. This operation helps check if two elements are in the same set.
    \item \texttt{union(u, v)}: Merges the sets containing elements $u$ and $v$. This operation is used to connect two elements, indicating that they are part of the same set.
\end{itemize}

\subsection{MCTC}
\begin{verbatim}
    Player X move:
. . . . .
 . . . . .
  . . X . .
   . . . . .
    . . . . .

Player O move:
. . . O .
 . . . . .
  . . X . .
   . . . . .
    . . . . .

Player X move:
. . . O .
 . . . . .
  . . X X .
   . . . . .
    . . . . .

Player O move:
. . O O .
 . . . . .
  . . X X .
   . . . . .
    . . . . .

Player X move:
. . O O .
 . . . . .
  . X X X .
   . . . . .
    . . . . .

Player O move:
. . O O .
 . . . . .
  . X X X .
   . . . . .
    . . . . O

Player X move:
. . O O .
 . . . . .
  . X X X .
   . X . . .
    . . . . O

Player O move:
. . O O .
 . . . . .
  . X X X .
   . X . . .
    . O . . O

Player X move:
. . O O .
 . . . . .
  . X X X .
   . X X . .
    . O . . O

Player O move:
. . O O .
 . . . . .
  . X X X .
   O X X . .
    . O . . O

Player X move:
. . O O .
 . . . . .
  . X X X .
   O X X . .
    X O . . O

Player O move:
. . O O .
 . . . O .
  . X X X .
   O X X . .
    X O . . O

Player X move:
. . O O .
 . . . O .
  . X X X .
   O X X . .
    X O . X O

Player O move:
. . O O .
 . . . O .
  . X X X .
   O X X . O
    X O . X O

Player X move:
. . O O X
 . . . O .
  . X X X .
   O X X . O
    X O . X O

Player O move:
. O O O X
 . . . O .
  . X X X .
   O X X . O
    X O . X O

Player X move:
. O O O X
 . . . O X
  . X X X .
   O X X . O
    X O . X O

Game Over. Winner: X
\end{verbatim}


\begin{algorithm}[H]
\caption{Monte Carlo Tree Search (MCTS)}
\begin{algorithmic}[1]
\STATE \textbf{Input:} HexBoard $board$, $exploration\_weight$
\STATE Initialize $Q \leftarrow$ defaultdict(int)
\STATE Initialize $N \leftarrow$ defaultdict(int)
\STATE Initialize $children \leftarrow$ dict()
\STATE Initialize $exploration\_weight \leftarrow 1$
\WHILE{not $board.is\_terminal()$}
    \FOR{$i = 1$ to $50$}
        \STATE do\_rollout($board$)
    \ENDFOR
    \STATE $board \leftarrow choose(board)$
    \STATE Print "Player X move:"
    \STATE Print $board.to\_pretty\_string()$
    \IF{$board.is\_terminal()$}
        \STATE Print "Game Over. Winner:", "X" if $board.winner$ else "O"
        \STATE \textbf{break}
    \ENDIF
    \FOR{$i = 1$ to $50$}
        \STATE do\_rollout($board$)
    \ENDFOR
    \STATE $board \leftarrow choose(board)$
    \STATE Print "Player O move:"
    \STATE Print $board.to\_pretty\_string()$
    \IF{$board.is\_terminal()$}
        \STATE Print "Game Over. Winner:", "X" if $board.winner$ else "O"
        \STATE \textbf{break}
    \ENDIF
\ENDWHILE

\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{do\_rollout(node)}
\begin{algorithmic}[1]
\STATE $path \leftarrow$ select($node$)
\STATE $leaf \leftarrow$ last node in $path$
\STATE expand($leaf$)
\STATE $reward \leftarrow$ simulate($leaf$)
\STATE backpropagate($path$, $reward$)
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{select(node)}
\begin{algorithmic}[1]
\STATE $path \leftarrow$ empty list
\WHILE{True}
    \STATE Append $node$ to $path$
    \IF{$node \notin children$ or $children[node]$ is empty}
        \RETURN $path$
    \ENDIF
    \STATE $unexplored \leftarrow children[node] - children.keys()$
    \IF{$unexplored$ is not empty}
        \STATE $n \leftarrow$ pop from $unexplored$
        \STATE Append $n$ to $path$
        \RETURN $path$
    \ENDIF
    \STATE $node \leftarrow$ uct\_select($node$)
\ENDWHILE
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{expand(node)}
\begin{algorithmic}[1]
\IF{$node \in children$}
    \RETURN
\ENDIF
\STATE $children[node] \leftarrow node.find\_children()$
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{simulate(node)}
\begin{algorithmic}[1]
\STATE $invert\_reward \leftarrow$ True
\WHILE{True}
    \IF{$node.is\_terminal()$}
        \STATE $reward \leftarrow node.reward()$
        \RETURN $1 - reward$ if $invert\_reward$ else $reward$
    \ENDIF
    \STATE $node \leftarrow node.find\_random\_child()$
    \STATE $invert\_reward \leftarrow \neg invert\_reward$
\ENDWHILE
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{backpropagate(path, reward)}
\begin{algorithmic}[1]
\FOR{$node$ in reversed($path$)}
    \STATE $N[node] \leftarrow N[node] + 1$
    \STATE $Q[node] \leftarrow Q[node] + reward$
    \STATE $reward \leftarrow 1 - reward$
\ENDFOR
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{uct\_select(node)}
\begin{algorithmic}[1]
\STATE $log\_N\_vertex \leftarrow \log(N[node])$
\STATE $uct \leftarrow$ function($n$):
    \STATE \hspace{1em} $Q[n] / N[n] + exploration\_weight \times \sqrt{log\_N\_vertex / N[n]}$
\RETURN $\max(children[node], key=uct)$
\end{algorithmic}
\end{algorithm}


\subsection{MCTC with RAVE algorithm}
So in this case we first implemented the RAVE algorithm that helps warm up tree faster: Rapid Action Value Estimation (RAVE) helps in sharing information among nodes that share the same move, leading to faster convergence.

The RAVE-adjusted score is calculated as follows:

\[
\text{score}(n) = (1 - \beta) \frac{Q(n)}{N(n)} + \beta \frac{RAVE\_Q(n)}{RAVE\_N(n)}
\]

where

\[
\beta = \frac{\text{rave\_factor}}{N(n) + RAVE\_N(n) + \text{rave\_factor}}
\]

Then i implemented several simulation strategy like Last Good Reply and also UCB1-Tuned. I integrate quality-based rewards, which consider the length of the simulation and the maximum number of actions. Quality-based Rewards for Monte-Carlo Tree Search Simulations which basically it asserts that we can apply discounted rewards by knowing the length of simulation and the maximum number of actions allowed to take in environment for each player (In some games, the game ends after limited number of moves. because there is no more movements).

\begin{algorithm}[H]
\caption{Monte Carlo Tree Search (MCTS) with RAVE}
\begin{algorithmic}[1]
\STATE \textbf{Input:} HexBoard $board$, $exploration\_weight$, $rave\_factor$
\STATE Initialize $Q \leftarrow$ defaultdict(int)
\STATE Initialize $N \leftarrow$ defaultdict(int)
\STATE Initialize $RAVE\_Q \leftarrow$ defaultdict(int)
\STATE Initialize $RAVE\_N \leftarrow$ defaultdict(int)
\STATE Initialize $children \leftarrow$ dict()
\STATE Initialize $exploration\_weight \leftarrow 1$
\STATE Initialize $rave\_factor \leftarrow 500$
\STATE Initialize $last\_good\_reply \leftarrow$ empty dict
\WHILE{not $board.is\_terminal()$}
    \FOR{$i = 1$ to $50$}
        \STATE do\_rollout($board$)
    \ENDFOR
    \STATE $board \leftarrow choose(board)$
    \STATE Print "Player X move:"
    \STATE Print $board.to\_pretty\_string()$
    \IF{$board.is\_terminal()$}
        \STATE Print "Game Over. Winner:", "X" if $board.winner$ else "O"
        \STATE \textbf{break}
    \ENDIF
    \FOR{$i = 1$ to $50$}
        \STATE do\_rollout($board$)
    \ENDFOR
    \STATE $board \leftarrow choose(board)$
    \STATE Print "Player O move:"
    \STATE Print $board.to\_pretty\_string()$
    \IF{$board.is\_terminal()$}
        \STATE Print "Game Over. Winner:", "X" if $board.winner$ else "O"
        \STATE \textbf{break}
    \ENDIF
\ENDWHILE

\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{do\_rollout(node)}
\begin{algorithmic}[1]
\STATE $path \leftarrow$ select($node$)
\STATE $leaf \leftarrow$ last node in $path$
\STATE expand($leaf$)
\STATE $reward, actions \leftarrow$ simulate($leaf$)
\STATE backpropagate($path$, $reward$, $actions$)
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{choose(node)}
\begin{algorithmic}[1]
\IF{$node.is\_terminal()$}
    \STATE \textbf{raise} RuntimeError("choose called on terminal node")
\ENDIF
\IF{$node \notin children$}
    \RETURN $node.find\_random\_child()$
\ENDIF
\STATE $best\_child \leftarrow \arg\max_{n \in children[node]}$ score($n$)
\STATE \textbf{return} $best\_child$
\STATE \textbf{function} score($n$)
    \IF{$N[n] == 0$}
        \STATE \textbf{return} $-\infty$
    \ENDIF
    \STATE $beta \leftarrow \frac{rave\_factor}{N[n] + RAVE\_N[n] + rave\_factor}$
    \STATE $q\_value \leftarrow \frac{Q[n]}{N[n]}$
    \STATE $rave\_value \leftarrow \frac{RAVE\_Q[n]}{RAVE\_N[n]}$ \textbf{if} $RAVE\_N[n] > 0$ \textbf{else} $0$
    \STATE \textbf{return} $(1 - beta) \times q\_value + beta \times rave\_value$
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{select(node)}
\begin{algorithmic}[1]
\STATE $path \leftarrow$ empty list
\WHILE{True}
    \STATE Append $node$ to $path$
    \IF{$node \notin children$ or $children[node]$ is empty}
        \RETURN $path$
    \ENDIF
    \STATE $unexplored \leftarrow children[node] - children.keys()$
    \IF{$unexplored$ is not empty}
        \STATE $n \leftarrow$ pop from $unexplored$
        \STATE Append $n$ to $path$
        \RETURN $path$
    \ENDIF
    \STATE $node \leftarrow$ uct\_select($node$)
\ENDWHILE
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{expand(node)}
\begin{algorithmic}[1]
\IF{$node \in children$}
    \RETURN
\ENDIF
\STATE $children[node] \leftarrow node.find\_children()$
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{simulate(node)}
\begin{algorithmic}[1]
\STATE $invert\_reward \leftarrow$ True
\STATE $actions \leftarrow$ empty set
\STATE $move\_count \leftarrow 0$
\WHILE{True}
    \IF{$node.is\_terminal()$}
        \STATE $reward \leftarrow node.reward() \times (0.9^{move\_count})$
        \RETURN $1 - reward$ \textbf{if} $invert\_reward$ \textbf{else} $reward$, $actions$
    \ENDIF
    \STATE $action \leftarrow node.find\_random\_child()$
    \STATE $actions.add(action.state)$
    \STATE $node \leftarrow action$
    \STATE $invert\_reward \leftarrow \neg invert\_reward$
    \STATE $move\_count \leftarrow move\_count + 1$
\ENDWHILE
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{backpropagate(path, reward, actions)}
\begin{algorithmic}[1]
\FOR{$node$ in reversed($path$)}
    \STATE $N[node] \leftarrow N[node] + 1$
    \STATE $Q[node] \leftarrow Q[node] + reward$
    \FOR{$action$ in $actions$}
        \STATE $RAVE\_N[action] \leftarrow RAVE\_N[action] + 1$
        \STATE $RAVE\_Q[action] \leftarrow RAVE\_Q[action] + reward$
    \ENDFOR
    \STATE $reward \leftarrow 1 - reward$
\ENDFOR
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{uct\_select(node)}
\begin{algorithmic}[1]
\STATE $log\_N\_vertex \leftarrow \log(N[node])$
\STATE $uct \leftarrow$ function($n$):
    \STATE \hspace{1em} $Q[n] / N[n] + exploration\_weight \times \sqrt{log\_N\_vertex / N[n]}$
\RETURN $\max(children[node], key=uct)$
\end{algorithmic}
\end{algorithm}

\section{Nested Rollout Policy Adaptation (NRPA) algorithm:}
The main loop continues until the game is terminal. In each iteration, the NRPA search is performed to find the best sequence of moves, and the first move of the sequence is applied to the board.

\begin{itemize}
    \item nrpa(self, level, policy, node): The core of the NRPA algorithm. It recursively searches for the best sequence of moves by performing rollouts and adapting the policy based on the observed rewards.

\item rollout(self, policy, node): Simulates a game from the given node (board state) following the provided policy until the game is terminal. It returns the reward of the final state and the sequence of moves made.

\item adapt(self, policy, sequence): Adjusts the policy based on the sequence of moves from a successful rollout. The adaptation process increases the probability of moves that led to a high reward.

\end{itemize}
An NRPA instance is created with a search depth of 3 and 10 iterations for policy adaptation.


\begin{algorithm}[H]
\caption{Nested Rollout Policy Adaptation (NRPA)}
\begin{algorithmic}[1]
\STATE \textbf{Input:} HexBoard $board$, $level$, $iterations$
\STATE Initialize $policy \leftarrow$ defaultdict(lambda: 1.0)
\STATE Initialize $nrpa \leftarrow$ NRPA(level=3, iterations=10)
\WHILE{not $board.is\_terminal()$}
    \STATE $score, sequence \leftarrow nrpa.search(policy, board)$
    \IF{$sequence$ is not empty}
        \STATE $board \leftarrow sequence[0]$
    \ENDIF
    \STATE Print "Player move:"
    \STATE Print $board.to\_pretty\_string()$
    \IF{$board.is\_terminal()$}
        \STATE Print "Game Over. Winner:", "X" if $board.winner$ else "O"
        \STATE \textbf{break}
    \ENDIF
\ENDWHILE
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{NRPA(level, policy, node)}
\begin{algorithmic}[1]
\IF{$level == 0$}
    \STATE $reward, sequence \leftarrow$ rollout($policy$, $node$)
    \RETURN $reward, sequence$
\ENDIF
\STATE $best\_score \leftarrow -\infty$
\STATE $best\_sequence \leftarrow$ empty list
\FOR{$i = 1$ to $iterations$}
    \STATE $new\_policy \leftarrow policy.copy()$
    \STATE $score, sequence \leftarrow$ NRPA($level - 1$, $new\_policy$, $node$)
    \IF{$score > best\_score$}
        \STATE $best\_score \leftarrow score$
        \STATE $best\_sequence \leftarrow sequence$
        \STATE $policy \leftarrow$ adapt($policy$, $best\_sequence$)
    \ENDIF
\ENDFOR
\RETURN $best\_score, $best\_sequence$
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{rollout(policy, node)}
\begin{algorithmic}[1]
\STATE $sequence \leftarrow$ empty list
\WHILE{not $node.is\_terminal()$}
    \STATE $moves \leftarrow$ list($node.find\_children()$)
    \IF{$moves$ is empty}
        \BREAK
    \ENDIF
    \STATE $weights \leftarrow$ [policy[move] for move in moves]
    \STATE $total\_weight \leftarrow$ sum($weights$)
    \STATE $probabilities \leftarrow$ [weight / total\_weight for weight in weights]
    \STATE $move \leftarrow random.choices(moves, probabilities)[0]$
    \STATE $sequence.append(move)$
    \STATE $node \leftarrow move$
\ENDWHILE
\RETURN $node.reward(), sequence$
\end{algorithmic}
\end{algorithm}

\begin{algorithm}[H]
\caption{adapt(policy, sequence)}
\begin{algorithmic}[1]
\STATE $learning\_rate \leftarrow 1.0$
\FOR{$move$ in $sequence$}
    \STATE $policy[move] \leftarrow policy[move] + learning\_rate$
    \STATE $learning\_rate \leftarrow learning\_rate \times 0.9$
\ENDFOR
\RETURN $policy$
\end{algorithmic}
\end{algorithm}
