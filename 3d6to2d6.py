'''
Converts 3d6 to 2d6

Plan is for n-dice of n-faces to 2d6 conversion in future (or another n-dice n-face)
 - All that remains is to map NdN to 2d6
 - can already create NdN pairs and calculate shortest distance between pairs on any regular polygon (n-sides)
 - will likely need to map n-faces n-sides to k-simplex (ie: vertices of n-dimensional polytope)
'''

import matplotlib.pyplot as plt
import random


class Dice:
    def __init__(self, num, sides):
        self.num = num
        self.sides = sides
        self.d = list(self.roll(num, sides))
        self.plist = self.pairs(self.d)
        self.llist = self.lines(self.d)
        self.converted = self.twoify(self.d[0])
        print(self.d[0], '--> ', self.converted)

    def roll(self, n, s):
        print('Rolling ' + str(n) + 'd' + str(s) + '... ')
        return [sorted([random.randint(1, s) for _ in range(n)]), s]

    def dist(self, a, b, c):
        x = max(a, b) - min(a, b)
        y = c - x if x > c // 2 else x
        return y % c

    def pairs(self, x):
        return [[x[0][i], x[0][j]] for i in range(self.num) for j in range(self.num) if i < j]

    def lines(self, x):
        return [self.dist(x[0][i], x[0][j], x[1]) for i in range(self.num) for j in range(self.num) if i < j]

    def allsame(self, r):
        # take the roll, see if the values are all the same
        for i in range(len(r)):
            if r[i] != r[0]:
                return False
        return True

    # The following is a 3d6 to 2d6 conversion.  NdN to NdN not yet ready.
    def tri_num(self, n):
        return n * (n + 1) // 2

    def tet_num(self, n):
        return n * (n + 1) * (n + 2) // 6

    def twoify(self, r):
        # maps 3d6 to a range from 0 to 35, with all triples mapping to 0, thus [1,1]
        print('Converting to 2d6 ...')
        i, j, k = r
        if self.allsame(r):
            return [1, 1]
        if j == k:
            j = i
        convert = self.tet_num(5 - i) + self.tri_num(5 - j) + 5 - k + 2
        return [convert // self.sides + 1, convert % self.sides + 1]


# roll 10,000 times, then plot distribution
testlist = []

for i in range(10000):
    roll = Dice(3, 6)
    testlist.append(roll.converted[0] + roll.converted[1])

plt.hist(testlist, bins=11)
plt.show()
