'''
Number guessing game
- two positive integers between 1 and 9 are chosen
- player one gets sum, player two (or computer) gets product
- players share information by answering yes/no to whether or not they know the chosen integers

Need to finish "guessing" component, and to fix the display of information
Also need to include some sort of hint system for when specific numbers are chosen
- certain number pairs cannot be guessed, and end up being a 50/50 chance
'''

import numpy as np
import random


class Game(object):
    def __init__(self):
        self.number = [random.randint(1, 9), random.randint(1, 9)]
        self.psmtrx = [np.arange(1, 10) * np.arange(1, 10).reshape(9, 1),
                       np.arange(1, 10) + np.arange(1, 10).reshape(9, 1)]
        self.psclue = [self.number[0] * self.number[1], sum(self.number)]
        self.pshint = [[(i, j) for (i, j) in np.ndenumerate(self.psmtrx[0]) if i[0] <= i[1]],
                       [(x, y) for (x, y) in np.ndenumerate(self.psmtrx[1]) if x[0] <= x[1]]]
        self.guess_list = list()

    def m_filter(self, a, b):
        # filtering inside of numpy.count_nonzero is super hacky... not guaranteed to work in future; need to rework
        if b == 0:
            return [a[y, z] for y in range(9) for z in range(9) if np.count_nonzero(a != a[y][z]) != 80]
        elif b == 1:
            return [a[y, z] for y in range(9) for z in range(9) if np.count_nonzero(a != a[y][z]) == 80]
        else:
            print('second argument must be 0 (for unique) or 1 (for non-unique)')
'''
    def guess(self, g):
        if (len(g) + 1) % 2 != 0:
            g.append(input('Do you know the numbers? (y/n): '))
            if g[len(g) - 1] == 'y':
                final = input('Final guess: ')
                if int(final) == self.psclue[0]:
                    print('You win!')
                else:
                    print('Nope, you lose! \nBetter luck next time! \nIt was actually ' + str(self.psclue[0]))
            else:
                self.m_filter(self.psmtrx[0], 0)
        else:
            g.append('n')
            self.m_filter(self.psmtrx[1], 0)
            guess()
        # this if statement no longer works -- update to check hint list instead of clue matrix
        if np.count_nonzero(clue_prod_matrix * filter_no_unique) == 1:
            print('Computer has won.')
            sum_num = np.argwhere(clue_prod_matrix * filter_no_unique != 0)[0]
            your_num = sum_num[0] + sum_num[1] + 2
            print('Your number was: ' + str(your_num))
        self.show_matrix()

    def show_matrix(self):
        print(clue_sums_matrix * filter_no_unique)
'''

newgame = Game()

print('Your secret number is: ' + str(newgame.psclue[1]))