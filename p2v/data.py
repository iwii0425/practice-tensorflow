import os
from collections import defaultdict, Counter

def build_vocab():
    # download data
    if not os.path.isfile('scripts.txt'):
        from subprocess import call
        call(["python", "downloader.py"])

    # load data
    scripts = defaultdict()
    with open('scripts.txt') as f:
        for l in f.readlines():
            character, line = l.split('\t', 1)
            scripts.setdefault(character, []).append(line.strip())

    # build a vocaburary
    words = []
    for lines in scripts.values():
        for line in lines:
            words.extend(word for word in line.split())
    vocab = Counter(words)

    # build word indexing
    idx2word = {}
    idx = 0
    for word in vocab.keys():
        idx2word[idx] = word
        idx += 1
    word2idx = dict((v, k) for k, v in idx2word.iteritems())

    # make data with indicies
    data = defaultdict()
    for character, lines in scripts.items():
        for line in lines:
            data.setdefault(character, []).extend(word2idx[word] for word in line.split())

    # make negative sampled data
    unique_data = {}
    unique_neg_data = {}

    for character, lines in data.items():
        unique_data[character] = list(set(lines))
    for character, lines in unique_data.items():
        unique_neg_data[character] = list(set(range(len(vocab))) - set(lines))

    return data, unique_neg_data, idx2word, word2idx, vocab
