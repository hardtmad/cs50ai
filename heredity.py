import csv
import itertools
import sys
import random

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_probability = 1
    for name, data in people.items():
        if name in two_genes: num_genes = 2
        elif name in one_gene: num_genes = 1
        else: num_genes = 0
        if name in have_trait: has_trait = True
        else: has_trait = False
        if data["mother"]==None and data["father"]==None:  # parents not in data set
            gene_prob = PROBS["gene"][num_genes]   # general pop gene prob
        else:  # parents in data set
            if data["mother"] in one_gene: num_mother_genes = 1
            elif data["mother"] in two_genes: num_mother_genes = 2
            else: num_mother_genes = 0
            if data["father"] in one_gene: num_father_genes = 1
            elif data["father"] in two_genes: num_father_genes = 2
            else: num_father_genes = 0
            gene_prob = child_gene_prob(num_mother_genes, num_father_genes, num_genes)
        jprob = gene_prob * PROBS["trait"][num_genes][has_trait]
        joint_probability *= jprob
    return joint_probability

def child_gene_prob(num_mother_genes, num_father_genes, num_child_genes):
    """
    Calculate and return the probability of a child having num_child_genes given
    parents have num_mother_genes and num_father_genes
    """
    probs = {}
    if num_mother_genes==0 and num_father_genes==0:
        probs[0] = 0.99 * 0.99  # both healthy, neither mutate
        probs[1] = (0.99 * 0.01) + (0.01 * 0.99)  # both healthy, exactly 1 mutates
        probs[2] = 0.01 * 0.01  # both healthy, both mutate
    elif num_mother_genes==1 and num_father_genes==1:
        probs[0] = (0.99 + 0.01)/2 * (0.01 + 0.99)/2  # 2 healthy no mut, 2 unhealthy both mut, 1 of each unhealthy muts healthy does not
        probs[1] = (0.5*(0.99 + 0.01)/2) + (0.5*(0.99 + 0.01)/2) # 2 healthy 1 muts, 2 unhealthy 1 muts, 1 of each and both or neither mut
        probs[2] = (0.99 + 0.01)/2 * (0.01 + 0.99)/2  # 2 unhealthy no mut, 2 healthy both mut, 1 of each healthy muts unhealthy does not
    elif num_mother_genes==2 and num_father_genes==2:
        probs[0] = 0.01 * 0.01  # both mutates
        probs[1] = 2*(0.99 * 0.01)   # exactly one mutates
        probs[2] = 0.99 * 0.99  # neither mutates
    elif (num_mother_genes==1 and num_father_genes==0) or (num_mother_genes==0 and num_father_genes==1):
        probs[0] = 0.99 * (0.99 + 0.01)/2  # 1 healthy doesn't mut AND 1 healthy that doesn't mut OR 1 unhealthy that does mut
        probs[1] = (0.01 * (0.99 + 0.01)/2) + (0.99 * (0.99 + 0.01)/2)  # 1 of each neither mutates or 2 healthy and 1 mutates
        probs[2] = 0.01 * (0.99 + 0.01)/2  # 1 healthy that mutates AND 1 healthy that does mut OR 1 unhealthy that doesn't
    elif (num_mother_genes==1 and num_father_genes==2) or (num_mother_genes==2 and num_father_genes==1):
        probs[0] = 0.01 * ((0.99 + 0.01)/2)  # 1 unhealthy that mutates AND 1 healthy that doesn't mut OR 1 unhealthy that does
        probs[1] = (0.01 * ((0.99 + 0.01)/2)) + (0.99 * ((0.99 + 0.01)/2))  # 1 of each neither mutates or 2 unhealthy and 1 mutates
        probs[2] = 0.99 * ((0.99 + 0.01)/2)  # 1 unhealthy doesn't mut AND 1 healthy that muts OR 1 unhealthy that doesn't mut
    elif (num_mother_genes==2 and num_father_genes==0) or (num_mother_genes==0 and num_father_genes==2):
        probs[0] = 0.99*0.01  # 1 of each and unhealthy mutates
        probs[1] = (0.99*0.99) + (0.01*0.01) # 1 of each and both or neither mutate
        probs[2] = 0.99*0.01  # 1 of each and healthy mutates
    return probs[num_child_genes]

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person, probs in probabilities.items():
        if person in two_genes: num_genes = 2
        elif person in one_gene: num_genes = 1
        else: num_genes = 0
        if person in have_trait: has_trait = True
        else: has_trait = False
        probs["gene"][num_genes] += p
        probs["trait"][has_trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Divide each value in the list by the sum of all values in the list
    for person, probs in probabilities.items():
        norm_val = 0
        for gVal in probs["gene"].values():
            norm_val += gVal
        for gKey, gVal in probs["gene"].items():
            probs["gene"][gKey] = gVal/norm_val
        norm_val = 0
        for tVal in probs["trait"].values():
            norm_val += tVal
        for tKey, tVal in probs["trait"].items():
            probs["trait"][tKey] = tVal/norm_val


if __name__ == "__main__":
    main()
