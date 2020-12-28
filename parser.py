import nltk
nltk.download('punkt')
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | DP VP | VP
S -> S Conj S
VP -> VP DP | VP PP | VP NP | Adv VP | VP Adv | V
DP -> Det NP
PP -> P NP | P DP
NP -> Adj NP | N
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = []
    for token in nltk.word_tokenize(sentence):
        if token.isalpha():
            words.append(token.lower())
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    sTrees = traverse_tree(tree)
    nps = []
    # Check which subtrees have label "NP" and do not contain NP subtrees
    for sTree in sTrees:
        if sTree.label() == "NP" and not find_lower_nps(sTree):
            nps.append(sTree)
    return nps


def traverse_tree(tree):
    """
    Recursively traverse an NLTK Tree and return a list of all subtrees.
    """
    so_far = []
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            so_far.append(subtree)
            sub2trees = traverse_tree(subtree)
            so_far.extend(sub2trees)
    return so_far


def find_lower_nps(tree):
    """
    Return True if there are NP subtrees in tree, otherwise return False.
    """
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            if subtree.label() == "NP" or find_lower_nps(subtree):
                return True
    return False


if __name__ == "__main__":
    main()
