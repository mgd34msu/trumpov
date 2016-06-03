import numpy as np
import random


class Game(object):
    def __init__(self):
        self.g_nums = self.get_nums()
        self.secret = [self.g_nums[0] * self.g_nums[1], sum(self.g_nums)]
        self.f_mask = self.filter_unique(self.get_array(0))
        self.player_array = self.get_array(1)
        self.comp_array = self.get_array(2)
        self.player_thinks = self.player_array * self.f_mask
        self.comp_thinks = self.comp_array * self.f_mask
        self.guess_list = []

    @staticmethod
    def get_nums():
        return [random.randint(1, 9), random.randint(1, 9)]

    @staticmethod
    def get_array(who):
        if who == 1:
            arr = np.arange(1, 10) * np.arange(1, 10).reshape(9, 1)
        elif who == 2:
            arr = np.arange(1, 10) + np.arange(1, 10).reshape(9, 1)
        else:
            return np.zeros((9, 9), dtype=np.int)
        for i in range(9):
            for j in range(9):
                if i > j:
                    arr[i][j] = 0
        return arr

    @staticmethod
    def filter_unique(f):
        for y in range(1, 10):
            for z in range(1, 10):
                if len([(y * z) / i for i in range(1, 10) if
                        (y * z) % i == 0 and (y * z) / i < 9 and i >= (y * z) / i]) < 2 or y > z:
                    f[y - 1, z - 1] = 0
                else:
                    f[y - 1, z - 1] = 1
        return f


class Player(object):
    def __init__(self, name):
        self.name = name
        self.money = 10
        self.wins = 0
        self.loss = 0
        self.w_l_ratio = self.wl(self.wins, self.loss)

    def wl(self, w, l):
        try:
            wlr = w / l
        except ZeroDivisionError:
            wlr = 0
        return wlr



def possibilities(a):
    return [[i, int(a / i)] for i in range(1, 10) if a % i == 0 and a / i < 9 and i >= a / i]


def best_guesses(a):
    return [sum(possibilities(a)[i]) for i in range(len(possibilities(a)))]


def initial_guess():
    print('Your secret number is: ' + str(player_secret))
    if player_secret in player_thinks:
        print(str(player_secret) + ' is not a unique product of any numbers between 1 and 9.')
        print('Continue guessing until you think you know the computer\'s secret number!')
        guess(guess_list)
    else:
        print(str(player_secret) + ' is the product of ' + str(game_numbers[0]) + ' and ' + str(game_numbers[1]) + '.')
        print('You know the computer\'s secret number is: ' + str(sum(game_numbers)) + '.')


def guess(g, helper=player_secret):
    if (len(g) + 1) % 2 != 0:
        print(best_guesses(helper))
        g.append(input('Do you know the numbers? (y/n): '))
        if g[len(g) - 1] == 'y':
            final = input('Final guess: ')
            if int(final) == computer_secret:
                print('You win!')
            else:
                print('Nope, you lose! \nBetter luck next time! \nIt was actually ' + str(computer_secret))
                return
                # else:
                # filter_matrix = m_filter(generate_matrix(2) * filter_matrix)
                # guess(g)
    else:
        g.append('n')
        print('WE NEED TO FILTER HERE TOO ... ')
        guess(g)


initial_guess()
