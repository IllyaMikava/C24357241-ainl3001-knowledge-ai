"""
TU850-3
AINL3001 — Knowledge-Driven AI
Week 4 Tutorial: Introducing the Problem Class
"""

from common.problem import Problem


GRID_SIZE = 5


class GridProblem(Problem):
    """
    A simple grid-world problem.

    A state is an (x, y) coordinate.
        (0, 0) = top-left corner
        (4, 4) = bottom-right corner

    x grows to the right, y grows DOWNWARD.
    """

    def actions(self, state):
        """Return the list of valid action names from this state."""
        x, y = state
        valid = []

        if y > 0:                  # not on the top row
            valid.append("UP")
        if y < GRID_SIZE - 1:      # not on the bottom row
            valid.append("DOWN")
        if x > 0:                  # not on the left column
            valid.append("LEFT")
        if x < GRID_SIZE - 1:      # not on the right column
            valid.append("RIGHT")

        return valid

    def result(self, state, action):
        """Return the new state produced by performing an action."""
        x, y = state

        if action == "UP":
            return (x, y - 1)
        if action == "DOWN":
            return (x, y + 1)
        if action == "LEFT":
            return (x - 1, y)
        if action == "RIGHT":
            return (x + 1, y)

        return state  # unknown action: stay where we are


# --------------------------------------------------
# CREATE A PROBLEM
# --------------------------------------------------

problem = GridProblem(
    initial=(0, 0),
    goal=(4, 4)
)


# --------------------------------------------------
# EXPLORE THE PROBLEM
# --------------------------------------------------

print("Initial state:", problem.initial)
print("Goal:", problem.goal)

print("\nActions from (0, 0):")
actions = problem.actions((0, 0))
print(actions)

print("\nResults of those actions:")
if actions is not None:
    for action in actions:
        new_state = problem.result((0, 0), action)
        print(action, "->", new_state)

print("\nIs (4, 4) the goal?")
print(problem.goal_test((4, 4)))

# --------------------------------------------------
# REFLECTION QUESTIONS
# --------------------------------------------------

"""
Be ready to discuss:

1. What information is stored in problem.initial?

2. What information is stored in problem.goal?

3. What is the difference between:

       problem.actions(state)

   and:

       problem.result(state, action)

4. Why doesn't Problem know anything about grids?

5. Why doesn't GridProblem know anything about search?

6. Could the same Problem structure be used for something
   other than a grid?
"""