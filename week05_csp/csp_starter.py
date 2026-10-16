"""
AINL3001 — Knowledge-Driven AI
Week 5 — Constraint Satisfaction Problems
BSP 2026

Australian map colouring: six regions and three colours.
"""

# --------------------------------------------------
# TASK 0 — MANUAL EXPLORATION
# --------------------------------------------------

example_assignment = {
    "WA": "Red",
    "NT": "Red",
    "SA": "Green",
    "Q": "Blue",
    "NSW": "Red",
    "V": "Green",
}

print("Manual CSP Exploration")
print(example_assignment)
print("\nQuestions:")
print("1. Is this assignment valid?")
print("2. Which neighbouring pairs violate a constraint?")
print("3. How could you correct the assignment?")
print("4. Why is it useful to detect violations early?")

# Task 0 answers:
# 1. No, it is not valid.
# 2. WA-NT (both Red) and SA-V (both Green).
# 3. NT has no free colour (WA=Red, SA=Green, Q=Blue), so change the
#    neighbours instead: WA -> Blue and V -> Blue. Now every pair differs.
# 4. A violation in a partial assignment means NO completion can work, so
#    we can abandon that whole branch without exploring it.

# --------------------------------------------------
# TASK 1 — CSP REPRESENTATION
# --------------------------------------------------

variables = ["WA", "NT", "SA", "Q", "NSW", "V"]

domains = {
    variable: ["Red", "Green", "Blue"]
    for variable in variables
}

constraints = [
    ("WA", "NT"),
    ("WA", "SA"),
    ("NT", "SA"),
    ("NT", "Q"),
    ("SA", "Q"),
    ("SA", "NSW"),
    ("SA", "V"),
    ("Q", "NSW"),
    ("NSW", "V"),
]

# --------------------------------------------------
# TASK 2 — CONSTRAINT CHECKING
# --------------------------------------------------

def is_valid_assignment(assignment):
    """Return True if a complete OR partial assignment is valid."""
    for a, b in constraints:
        if a in assignment and b in assignment:
            if assignment[a] == assignment[b]:
                return False
    return True


# --------------------------------------------------
# TASK 3 AND TASK 5 — VARIABLE SELECTION
# --------------------------------------------------

def select_unassigned_variable(assignment):
    """Choose the next unassigned region using MRV
    (Minimum Remaining Values). Ties go to the earliest region in
    `variables`. Returns None if everything is assigned.
    """
    best_variable = None
    best_count = None

    for variable in variables:
        if variable in assignment:
            continue

        # Count currently legal colours for this variable.
        legal_count = 0
        for colour in domains[variable]:
            assignment[variable] = colour       # temporary assignment
            if is_valid_assignment(assignment):
                legal_count += 1
            del assignment[variable]            # undo

        # Strict "<" keeps the first variable on ties.
        if best_count is None or legal_count < best_count:
            best_variable = variable
            best_count = legal_count

    return best_variable

    # Task 3 version (simple, first unassigned):
    # for variable in variables:
    #     if variable not in assignment:
    #         return variable
    # return None


# --------------------------------------------------
# TASK 3 — BACKTRACKING SEARCH
# --------------------------------------------------

def backtracking_search(assignment):
    """Return a complete valid assignment, or None if none exists."""
    if len(assignment) == len(variables):
        return dict(assignment)  # return a COPY

    variable = select_unassigned_variable(assignment)

    for colour in domains[variable]:
        assignment[variable] = colour
        if is_valid_assignment(assignment):
            result = backtracking_search(assignment)
            if result is not None:
                return result
        del assignment[variable]  # backtrack

    return None


# --------------------------------------------------
# TASK 4 — BRUTE FORCE COMPARISON
# --------------------------------------------------

# Brute force checks all 3 ** 6 = 729 complete assignments.
# Backtracking checks constraints after EACH assignment, so as soon as a
# partial assignment breaks a constraint (e.g. WA=Red, NT=Red) it prunes
# every completion of it. That one failure skips 3 ** 4 = 81 complete
# assignments without ever generating them.

def brute_force_count():
    """Count how many of the 729 complete assignments are valid."""
    from itertools import product
    valid = 0
    for colours in product(["Red", "Green", "Blue"], repeat=len(variables)):
        if is_valid_assignment(dict(zip(variables, colours))):
            valid += 1
    return valid


# --------------------------------------------------
# TESTING AREA
# --------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("WEEK 5 — CONSTRAINT SATISFACTION PROBLEMS")
    print("=" * 50)

    print("\nVariables:", variables)
    print("Domains:", domains)
    print("Constraints:", constraints)

    print("\nExample assignment valid?")
    print(is_valid_assignment(example_assignment))  # Expected: False

    partial_assignment = {"WA": "Red", "NT": "Green"}
    print("\nPartial assignment valid?")
    print(is_valid_assignment(partial_assignment))  # Expected: True

    print("\nSearching for a solution...")
    solution = backtracking_search({})
    print("Solution:", solution)

    if solution is not None:
        print("\nSolution valid?", is_valid_assignment(solution))
        print("\nColour assignment:")
        for region in variables:
            print(f"{region:4} -> {solution[region]}")
    else:
        print("No solution found.")

    print("\nPossible complete assignments:", 3 ** len(variables))
    print("Valid complete assignments (brute force):", brute_force_count())

    print("\nReflection:")
    print("1. What causes backtracking?")
    print("   A partial assignment violates a constraint (or a variable has")
    print("   no legal colour left), so we undo the last choice and try the next.")
    print("2. Why can backtracking be faster than brute force?")
    print("   It prunes: one bad partial assignment eliminates every complete")
    print("   assignment that extends it, instead of testing them one by one.")
    print("3. Why might MRV reduce search?")
    print("   It picks the most constrained region first (fail-first), so dead")
    print("   ends are found early, high in the tree, where pruning saves most.")
    print("4. How could this model represent timetabling?")
    print("   Variables = classes/exams, domains = time slots (and rooms),")
    print("   constraints = two classes sharing a student or lecturer cannot")
    print("   share a slot (the same 'different value' constraint as neighbours).")