from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # World knowledge
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # Statement
    Biconditional(AKnight, And(AKnight, AKnave))  # 1. A says "I am both a knight and a knave."
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # World knowledge
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # Statement
    Biconditional(AKnight, And(AKnave, BKnave))  # 1. A says "We are both knaves."
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # World knowledge
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # Statements
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),  # 1. A says "We are the same kind."
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))  # 2. B says "We are of different kinds."
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # World Knowledge
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    # Statements
    Or(
        And(Implication(AKnight, AKnight), Implication(AKnave, Not(AKnight))),  # A says "I am a knight" (could be truth or lie)
        And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))  # A says "I am a knave" (could be truth or lie)
        ),  # 1. A says either "I am a knight." or "I am a knave.", but you don't know which.
    Biconditional(
        BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))
        ),  #  2. B says "A said 'I am a knave'."
    Biconditional(BKnight, CKnave),  # 3. B says "C is a knave."
    Biconditional(CKnight, AKnight)  # 4. C says "A is a knight."
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
