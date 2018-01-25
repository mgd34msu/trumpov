import json
import random as rnd

chain = {}
corpus = []

data = json.load(open('condensed.json'))

for line in data:
    add_word = line['text'].replace('\r', ' ').replace('\n', ' ').replace('\"', '').split(' ')
    add_word = [word for word in add_word if word not in ['', ' ']]
    corpus = corpus + add_word

for i, k1 in enumerate(corpus):
    if len(corpus) > (i + 2):
        k2 = corpus[i + 1]
        word = corpus[i + 2]
        if (k1, k2) not in chain:
            chain[(k1, k2)] = [word]
        else:
            chain[(k1, k2)].append(word)


def trumpov(_chain=chain, _corpus=corpus, _msglen=140):
    _idx = rnd.randint(0, len(_corpus) - 1)
    _key = (_corpus[_idx], _corpus[_idx + 1])
    _msg = _key[0] + ' ' + _key[1]

    while len(_msg) < _msglen:
        _choice = rnd.choice(_chain[_key])
        _msg += ' ' + _choice
        _key = (_key[1], _choice)

    print(_msg)
