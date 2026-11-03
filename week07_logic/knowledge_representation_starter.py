#CILLIAN IS GOING TO DEMO NEXT WEEKS LAB FIRST 

"""AINL3001 — Topic 7: Knowledge Representation and Logical Reasoning.

Student starter: complete the TODOs in Tasks 3 and 4.
This lab uses propositional facts and simple IF/THEN rules.

BSP
2026
"""

# TASK 1 — Represent facts (provided; inspect and experiment).

# it starts with known facts and check every rule. if rule's conditions are satisfied, 
# it adds the conclusion to the known facts. It repeats until no new facts can be added.
facts = {"rainy", "weekday"}

# TASK 2 — Represent rules (provided; inspect and experiment).
# Each rule is (list_of_required_facts, conclusion).
# All conditions must be known before the conclusion can be inferred.
rules = [
    (["rainy"], "take_umbrella"),
    (["rainy", "cold"], "wear_coat"),
    (["take_umbrella"], "stay_dry"),
]


def forward_chaining(known_facts, rules):
    """Return all original and inferred facts without changing known_facts.

    TASK 3 — TODO:
    1. Copy known_facts into a new set.
    2. Examine every rule and add its conclusion when ALL conditions hold.
    3. Repeat until an entire pass adds no new facts.
    4. Return the completed set.
    """
    # Step 1: Copy the original facts into a new set
    inferred_facts = set(known_facts)

    # Step 2: Keep track of whether any new facts were added
    new_fact_added = True

    while new_fact_added:
        new_fact_added = False
        for conditions, conclusion in rules:
            # Check if all conditions are in the inferred_facts
            if all(condition in inferred_facts for condition in conditions):
                # If the conclusion is not already in inferred_facts, add it
                if conclusion not in inferred_facts:
                    inferred_facts.add(conclusion)
                    new_fact_added = True
    return inferred_facts


def query(inferred_facts, statement):
    """TASK 4 — Return True if statement is established in inferred_facts.

    A False result means 'not established', not necessarily 'false'.
    """
    return statement in inferred_facts


if __name__ == "__main__":
    print("=" * 55)
    print("TASK 0 — MANUAL REASONING")
    print("=" * 55)
    print("Initial facts:", sorted(facts))
    print("Rules:")
    for conditions, conclusion in rules:
        print(f"  IF {' AND '.join(conditions)} THEN {conclusion}")
    print("\nBefore coding, predict whether these can be inferred:")
    print("  take_umbrella?  stay_dry?  wear_coat?  Why?")

    print("\n" + "=" * 55)
    print("TASKS 3–4 — FORWARD CHAINING AND QUERIES")
    print("=" * 55)
    inferred = forward_chaining(facts, rules)
    if inferred is None:
        print("Complete forward_chaining() to see inferred knowledge.")
    else:
        print("Initial facts:", sorted(facts))
        print("All known facts:", sorted(inferred))
        for statement in ("take_umbrella", "stay_dry", "wear_coat"):
            print(f"Can infer {statement}? {query(inferred, statement)}")

    print("\nTASK 5 — BACKWARD CHAINING (discussion)")
    print("Goal: stay_dry. Which rule concludes it? What must be true first?")
    print("\nTASK 6 — LOGIC DISCUSSION")
    print("Is 'IF rainy THEN take_umbrella' always true in the real world?")
    print("What assumptions does the rule make?")