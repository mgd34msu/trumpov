from collections import defaultdict
import glob
import json
import random as rnd

order = 2
msglen = 160
corpus = list()
punct_list = ['.', '!', '?']
chain = defaultdict(list)
files = glob.glob('c:\\temp\\prj\\devfiles\\sf\\201*.json')

for element in files:
    data = json.load(open(element, encoding='UTF-8'))
    for line in data:
        if line['user'] == 'U03GTMQL8':
            add_word = line['text'].replace('\r', ' ').replace('\n', ' ').replace('\"', '').replace('&amp;', '&').split(' ')
            add_word = [word for word in add_word if word not in ['', ' ']]
            corpus = corpus + add_word
        else:
            print('next...\n')

    for i in range(len(corpus) - order):
        chain[tuple(corpus[i:i + order])].append(corpus[i + order])


    def fazmov(_chain=chain, _corpus=corpus, _order=order, _msglen=msglen):
        _idx = rnd.randint(0, len(_corpus) - _order)
        while not _corpus[_idx].isupper():
            _idx = rnd.randint(0, len(_corpus) - _order)
        _key = _corpus[_idx:_idx + _order]

        for _ in range(_msglen):
            if len(' '.join(_key)) < _msglen:
                if len(' '.join(_key)) > 100:
                    if ' '.join(_key)[-1] not in punct_list:
                        _key.append(rnd.choice(_chain[tuple(_key[-_order:])]))
                else:
                    _key.append(rnd.choice(_chain[tuple(_key[-_order:])]))

        _msg = ' '.join(_key)
        print(_msg)
