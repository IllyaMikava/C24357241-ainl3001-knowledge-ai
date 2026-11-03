
"""
AINL3001 — Knowledge-Driven AI
Week 6 — Adversarial Search (Tic-Tac-Toe)
BSP 2026

X is MAX (+1 for a win); O is MIN (-1 for a win).
A draw has utility 0. Both players play optimally.
"""

# TASK 0 — MANUAL MINIMAX

print("=" * 50)
print("TASK 0 — MANUAL MINIMAX")
print("=" * 50)

print(r"""
             3
           /   \
          3     2
        /  \   /  \
       3    5  2    9
""")

print("MIN nodes return: 3 and 2")
print("MAX chooses the left branch, with value 3.")


# INITIAL BOARD — X plays next

board = [
    "X", "O", "X",
    " ", "O", " ",
    " ", " ", "X",
]

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


# TASK 1 — BOARD REPRESENTATION

def print_board(state):
    """Display the board as a 3-by-3 grid."""
    for row in range(3):
        start = row * 3
        print(" | ".join(state[start:start + 3]))
        if row < 2:
            print("--+---+--")


# TASK 1 — AVAILABLE MOVES

def available_moves(state):
    """Return the indices of all empty cells."""
    return [i for i in range(9) if state[i] == " "]


# TASK 1 — MAKE A MOVE

def make_move(state, move, player):
    """Return a new board without modifying the original."""
    new_state = state.copy()
    new_state[move] = player
    return new_state


# TASK 2 — WINNER

def check_winner(state):
    """Return 'X', 'O', or None."""
    for a, b, c in WINNING_LINES:
        if state[a] != " " and state[a] == state[b] == state[c]:
            return state[a]
    return None


# TASK 2 — TERMINAL STATE

def is_terminal(state):
    """A game ends with a win or a full board."""
    return (
        check_winner(state) is not None
        or len(available_moves(state)) == 0
    )


# TASK 2 — UTILITY

def utility(state):
    """Return +1 for X, -1 for O, or 0 for a draw."""
    winner = check_winner(state)

    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    else:
        return 0


# TASK 3 — MINIMAX

def minimax(state, maximizing, counter):
    """Return the optimal score and count visited nodes."""
    counter["nodes"] += 1

    if is_terminal(state):
        return utility(state)

    if maximizing:  # X is MAX
        best_score = float("-inf")

        for move in available_moves(state):
            child = make_move(state, move, "X")
            score = minimax(child, False, counter)
            best_score = max(best_score, score)

        return best_score

    else:  # O is MIN
        best_score = float("inf")

        for move in available_moves(state):
            child = make_move(state, move, "O")
            score = minimax(child, True, counter)
            best_score = min(best_score, score)

        return best_score


# TASK 4 AND 5 — BEST MOVE USING MINIMAX

def best_move(state, counter):
    """Return the best move index for X, or None if game is over."""
    if is_terminal(state):
        return None

    best_score = float("-inf")
    best_index = None

    for move in available_moves(state):
        child = make_move(state, move, "X")
        score = minimax(child, False, counter)

        # Strict > preserves the first move when scores tie.
        if score > best_score:
            best_score = score
            best_index = move

    return best_index


# TASK 6 — ALPHA-BETA PRUNING

def alpha_beta(state, maximizing, alpha, beta, counter):
    """Minimax with alpha-beta pruning."""
    counter["nodes"] += 1

    if is_terminal(state):
        return utility(state)

    if maximizing:  # X is MAX
        best_score = float("-inf")

        for move in available_moves(state):
            child = make_move(state, move, "X")
            score = alpha_beta(
                child, False, alpha, beta, counter
            )

            best_score = max(best_score, score)
            alpha = max(alpha, best_score)

            if alpha >= beta:
                break  # Prune remaining branches

        return best_score

    else:  # O is MIN
        best_score = float("inf")

        for move in available_moves(state):
            child = make_move(state, move, "O")
            score = alpha_beta(
                child, True, alpha, beta, counter
            )

            best_score = min(best_score, score)
            beta = min(beta, best_score)

            if alpha >= beta:
                break  # Prune remaining branches

        return best_score


# TASK 6 — BEST MOVE USING ALPHA-BETA

def best_move_alpha_beta(state, counter):
    """Return the best move index for X using alpha-beta."""
    if is_terminal(state):
        return None

    best_score = float("-inf")
    best_index = None
    alpha = float("-inf")
    beta = float("inf")

    for move in available_moves(state):
        child = make_move(state, move, "X")

        score = alpha_beta(
            child, False, alpha, beta, counter
        )

        if score > best_score:
            best_score = score
            best_index = move

        # X has found a better guaranteed score.
        alpha = max(alpha, best_score)

    return best_index


# TESTING

if __name__ == "__main__":
    print("\nCurrent board (X to move):")
    print_board(board)

    print("\nAvailable moves:", available_moves(board))
    print("Winner:", check_winner(board))
    print("Terminal:", is_terminal(board))
    print("Utility:", utility(board))

    # Minimax search
    minimax_counter = {"nodes": 0}
    move_minimax = best_move(board, minimax_counter)

    print("\nMinimax best move for X:", move_minimax)
    print("Minimax nodes visited:", minimax_counter["nodes"])

    # Alpha-beta search
    alpha_beta_counter = {"nodes": 0}
    move_ab = best_move_alpha_beta(board, alpha_beta_counter)

    print("\nAlpha-Beta best move for X:", move_ab)
    print("Alpha-Beta nodes visited:", alpha_beta_counter["nodes"])

    # Show the board after the chosen move
    if move_minimax is not None:
        print("\nBoard after Minimax move:")
        print_board(make_move(board, move_minimax, "X"))

    # Reflection answers
    print("\nReflection:")

    print("1. Tic-Tac-Toe is a search problem because")
    print("   players explore possible moves and future states.")

    print("2. Minimax assumes an optimal opponent because")
    print("   it chooses moves against the strongest possible response.")

    print("3. A utility function assigns numerical values to")
    print("   terminal states so the algorithm can compare outcomes.")

    print("4. Larger games have much larger search trees,")
    print("   increasing computation time and memory requirements.")
