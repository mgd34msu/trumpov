from collections import defaultdict
import json
import random as rnd

order = 3
msglen = 140
corpus = list()
punct_list = ['.', '!', '?']

data = json.load(open('c:\\temp\\prj\\devfiles\\condensed.json'))

for line in data:
    if not line['is_retweet']:
        add_word = line['text'].replace('\r', ' ').replace('\n', ' ').replace('\"', '').replace('&amp;', '&').split(' ')
        add_word = [word for word in add_word if word not in ['', ' ']]
        corpus = corpus + add_word

chain = defaultdict(list)

for i in range(len(corpus) - order):
    chain[tuple(corpus[i:i + order])].append(corpus[i + order])


def trumpov(_chain=chain, _corpus=corpus, _order=order, _msglen=msglen):
    _idx = rnd.randint(0, len(_corpus) - _order)
    while not _corpus[_idx].isupper():
        _idx = rnd.randint(0, len(_corpus) - _order)
    _key = _corpus[_idx:_idx + _order]

    for _ in range(_msglen):
        if len(' '.join(_key)) < _msglen:
            if len(' '.join(_key)) > 100:
                if ' '.join(_key)[-1] not in punct_list:
                    _key.append(rnd.choice(_chain[tuple(_key[-order:])]))
            else:
                _key.append(rnd.choice(_chain[tuple(_key[-order:])]))

    _msg = ' '.join(_key)
    print(_msg)
