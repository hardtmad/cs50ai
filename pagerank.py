import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_linked_pages = len(corpus[page])
    num_total_pages = len(corpus.keys())
    if num_linked_pages == 0: #  equal probability for all pages
        linked_prob = 0
        unlinked_prob = 1/num_total_pages
    else:
        linked_prob = damping_factor/num_linked_pages
        unlinked_prob = (1-damping_factor)/num_total_pages
    transition_dict = {}
    for pg in corpus.keys():
        if pg in corpus[page]:  # linked page case
            transition_dict[pg] = linked_prob + unlinked_prob
        else:  # not linked page case
            transition_dict[pg] = unlinked_prob
    return transition_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    hits = {}  # track # of hits per page
    tModels = {}   # store transition models
    for page in corpus.keys():
        hits[page] = 0  # init to 0
        tModels[page] = transition_model(corpus, page, damping_factor)
    # Randomly get the first sample
    random.seed()  # init the random number generator based on system time
    firstIdx = random.randint(0, (len(corpus.keys())-1))
    curSample = list(corpus.keys())[firstIdx]
    samplesRemaining = SAMPLES - 1
    while samplesRemaining>=0:
        hits[curSample] += 1  # increment hits for current sample
        # Generate the next sample
        curSample = random.choices(list(corpus.keys()), tModels[curSample].values())[0]
        samplesRemaining -= 1
    # Normalize hits based on # SAMPLES and round to 4 decimal places
    for pg, count in hits.items():
        hits[pg] = hits[pg]/SAMPLES
    return hits


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize Page Rank with naive 1/N assumption
    ranks = {}
    num_total_pages = len(corpus.keys())
    for page in corpus.keys():
        ranks[page] = 1/num_total_pages
    # Iterate until we don't see any deltas greater than 0.001
    max_delta = 1
    while max_delta>0.001:
        max_delta = -1 # reset max_delta for each iteration
        orig_ranks = copy.deepcopy(ranks)
        for page in corpus.keys():
            randomProb = (1-damping_factor)/num_total_pages
            linkProb = 0
            for p in corpus.keys():
                if page in corpus[p]:  # found a page that links to current page
                    linkProb += orig_ranks[p]/len(corpus[p])
            linkProb = damping_factor * linkProb
            ranks[page] = randomProb + linkProb
            # Update max delta seen this iteration
            page_delta = abs(orig_ranks[page] - ranks[page])
            max_delta = max(max_delta, page_delta)
    return orig_ranks  # return values before last iteration


if __name__ == "__main__":
    main()
