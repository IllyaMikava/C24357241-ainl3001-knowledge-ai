"""
AINL3001 — Knowledge-Driven AI
Week 4 — Local Search and Optimisation
BSP 2026

This week introduces local search.

In previous weeks, search algorithms explored paths through
a state space in order to reach a goal.

Local search takes a different approach:

    1. Start with a state.
    2. Evaluate how good that state is.
    3. Generate neighbouring states.
    4. Move to a better neighbour.
    5. Repeat.

We will explore this using the N-Queens problem.

Tasks
-----

1. Understand the problem representation.
2. Implement conflict counting.
3. Explore neighbouring states.
4. Implement Hill Climbing.
5. Implement Simulated Annealing.
"""

import math
import random

from queens_problem import QueensProblem

N = 8


# --------------------------------------------------
# TASK 0 — UNDERSTANDING THE STATE
# --------------------------------------------------

example_board = [0, 1, 2, 3]

print("Manual Exploration Board:")
print(example_board)

print(
    "\nEach list position represents a column."
)

print(
    "Each value represents the row containing the queen."
)

print(
    "\nQuestion: How many conflicts exist on this board?"
)


# --------------------------------------------------
# TASK 1 — EVALUATE A STATE
# --------------------------------------------------

def count_conflicts(board):
    """
    Return the number of pairs of queens
    that attack each other.

    Lower values are better.

    A solution has:

        conflict count = 6
    """

    conflicts = 0

    for i in range(len(board)):
        for j in range(i + 1, len(board)):

            same_row = board[i] == board[j]

            same_diagonal = (
                abs(board[i] - board[j])
                == abs(i - j)
            )

            if same_row or same_diagonal:
                conflicts += 1

    return conflicts

    pass


# --------------------------------------------------
# TASK 2 — EXPLORE THE PROBLEM
# --------------------------------------------------

def generate_neighbours(problem, board):
    """
    Generate all neighbouring boards.

    Use the Problem interface introduced this week:

        problem.actions(state)
        problem.result(state, action)
    """
    neighbours = []

    actions = problem.actions(board)

    for action in actions:

        neighbour = problem.result(
            board,
            action
        )

        neighbours.append(neighbour)

    return neighbours


# --------------------------------------------------
# TASK 3 — HILL CLIMBING
# --------------------------------------------------

def hill_climbing(problem, start_board):
    """
    Use Hill Climbing to reduce the number
    of conflicts.

    Algorithm:

        current = start state

        repeat:

            generate neighbours

            find the neighbour with the
            lowest conflict count

            if the neighbour is not better:
                stop

            otherwise:
                move to the neighbour

        return current
    """

    current = start_board

    while True:

        neighbours = generate_neighbours(
            problem,
            current
        )

        best_neighbour = min(
            neighbours,
            key=count_conflicts
        )

        if count_conflicts(best_neighbour) >= count_conflicts(current):
            break

        current = best_neighbour

    return current


# --------------------------------------------------
# TASK 4 — SIMULATED ANNEALING
# --------------------------------------------------

def simulated_annealing(problem, start_board):
    """
    Use Simulated Annealing to search for
    a solution.

    Unlike Hill Climbing, Simulated Annealing
    can sometimes accept a worse state.

    This can help escape local minima.
    """

    current = start_board

    temperature = 10.0
    cooling_rate = 0.95

    while temperature > 0.1:

        neighbours = generate_neighbours(
            problem,
            current
        )

        next_board = random.choice(
            neighbours
        )

        current_cost = count_conflicts(
            current
        )

        next_cost = count_conflicts(
            next_board
        )

        delta = next_cost - current_cost

        if delta < 0:

            current = next_board

        else:

            probability = math.exp(
                -delta / temperature
            )

            if random.random() < probability:
                current = next_board

        temperature *= cooling_rate

    return current


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------
if __name__ == "__main__":

    board = [
        random.randint(0, N - 1)
        for _ in range(N)
    ]

    problem = QueensProblem(board)

    print("\nRandom Board")
    print(board)

    print("\nConflicts")
    print(
        count_conflicts(board)
    )

    print("\nPossible Actions")

    actions = problem.actions(board)

    print(
        f"{len(actions)} actions available"
    )

    print("\nNeighbours")

    neighbours = generate_neighbours(
        problem,
        board
    )

    print(
        f"{len(neighbours)} neighbours generated"
    )
    
start_cost = count_conflicts(board)

print("Start Cost:", start_cost)

# --------------------
# Hill Climbing
# --------------------

hill_result = hill_climbing(problem, board)

hill_final_cost = count_conflicts(hill_result)

print("\nHill Climbing")
print("Final Board:")
print(hill_result)
print("Final Cost:", hill_final_cost)

# --------------------
# Simulated Annealing
# --------------------

annealing_result = simulated_annealing(problem, board)

annealing_final_cost = count_conflicts(annealing_result)

print("\nSimulated Annealing")
print("Final Board:")
print(annealing_result)
print("Final Cost:", annealing_final_cost)