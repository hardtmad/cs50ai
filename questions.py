import nltk
import sys
import os
import string
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    contents = {}
    for fn in os.listdir(directory):
        fp =  os.path.join(directory, fn)
        # Skip anything that's not a .txt file
        if not os.path.isfile(fp) or not fp.endswith(".txt"):
            continue
        with open (fp, "r") as inF:
            contents[fn] = inF.read()
    return contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = []
    for token in nltk.word_tokenize(document):
        # Remove common unhelpful words
        if not token in nltk.corpus.stopwords.words("english"):
            # Remove punctuation
            for punct in string.punctuation:
                token = token.replace(punct, '')
            if token != "":
                words.append(token.lower())
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    doc_freqs = {}
    total_docs = 0
    for k, v in documents.items():
        total_docs += 1
        # Cast the list of words to a set so each word appears only once
        word_set = set(v)
        for word in word_set:
            # Init if we haven't seen this word before
            if word not in doc_freqs:
                doc_freqs[word] = 0
            # Increment # of documents where this word has been seen
            doc_freqs[word] += 1
    for k, v in doc_freqs.items():
        # Calulate IDF = ln(total_docs/doc_freqs)
        idfs[k] = log(total_docs/v)
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = {}
    for file_name, file_words in files.items():
        file_tfidf = 0
        for word in query:
            if word not in file_words:
                continue
            tf = file_words.count(word)
            # Calculate tf-idf
            tfidf = tf * idfs[word]
            file_tfidf += tfidf
        file_scores[file_name] = file_tfidf
    # Sort files by highest tf-idf scores
    file_scores = dict(sorted(file_scores.items(), key=lambda item: item[1], reverse=True))
    # Return list files with top n scores
    return list(file_scores.keys())[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sen_scores = {}
    for sentence, sen_words in sentences.items():
        sen_scores[sentence] = 0
        for word in query:
            if word not in sen_words or word in nltk.corpus.stopwords.words("english"):
                continue
            sen_scores[sentence] += idfs[word]
    # Sort sentences by highest idf scores
    sen_scores = dict(sorted(sen_scores.items(), key=lambda item: item[1], reverse=True))
    sen_list = list(sen_scores.keys())
    idx = 0
    prev_score, prev_sen = None, None
    final_list = []
    for cur_sen in sen_list:
        cur_score = sen_scores[cur_sen]
        # We only care if any of the top n sentences have tied scores
        if idx >= n and cur_score != prev_score:
            break
        # Figure out which to prefer for tied sentences
        if cur_score == prev_score:
            prev_qtd = query_term_density(query, sentences[prev_sen])
            cur_qtd = query_term_density(query, sentences[cur_sen])
            if prev_qtd < cur_qtd:
                # Switch the order
                final_list.pop()
                final_list.append(cur_sen)
                final_list.append(prev_sen)
        else:
            final_list.append(cur_sen)
        prev_score = cur_score
        prev_sen = cur_sen
        idx += 1
    if sen_scores[final_list[0]] == 0:
        return ["Sorry I don't know much about that topic. Feed me some sources and I can learn more!"]
    return final_list[:n]


def query_term_density(query, sentence):
    """
    Given a query (set of words) and sentence (set of words), return the query
    term density, the proportion of words in the sentence that are also words
    in the query.
    """
    num_words_sentence = len(sentence)
    num_words_sentence_query = 0
    for word in sentence:
        if word in query:
            num_words_sentence_query += 1
    return num_words_sentence_query/num_words_sentence


if __name__ == "__main__":
    main()
