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

    @staticmethod
    def possibilities(a):
        return [[i, int(a / i)] for i in range(1, 10) if a % i == 0 and a / i < 9 and i >= a / i]

    def best_guesses(self, a):
        return [sum(self.possibilities(a)[i]) for i in range(len(self.possibilities(a)))]


class Player(object):
    def __init__(self, name):
        self.name = name
        self.money = 10
        self.wins = 0
        self.loss = 0
        self.w_l_ratio = self.wl(self.wins, self.loss)
        self.current_bet = 0

    @staticmethod
    def wl(w, l):
        try:
            wlr = w / l
        except ZeroDivisionError:
            wlr = 0
        return wlr


player = Player(input('Player Name: '))
game = Game()


def bet():
    if player.money > 0:
        print('Max bet: ' + str(player.money) + '.')
        amount = input('Bet amount: ')
        if int(amount) > int(player.money):
            print('Unable to bet the specified amount.  Please try again.')
            amount = 0
            bet()
    else:
        print('Game Over')
        return 0, 0
    player.current_bet = int(amount)
    player.money -= int(amount)
    return player.current_bet, player.money


def guess(g, helper=game.secret[0]):
    if (len(g) + 1) % 2 != 0:
        print(game.best_guesses(helper))
        g.append(input('Do you know the numbers? (y/n): '))
        if g[len(g) - 1] == 'y':
            final = input('Final guess: ')
            if int(final) == game.secret[1]:
                print('You win!')
                player.money += player.current_bet * 2
                player.current_bet = 0
                return player.money, player.current_bet
            else:
                print('Nope, you lose! \nBetter luck next time! \nIt was actually ' + str(game.secret[1]))
                player.current_bet = 0
                return player.current_bet
                # else:
                # filter_matrix = m_filter(generate_matrix(2) * filter_matrix)
                # guess(g)
    else:
        g.append('n')
        print('WE NEED TO FILTER HERE TOO ... ')
        guess(g)


def initial_guess():
    player.current_bet, player.money = bet()
    print('Your secret number is: ' + str(game.secret[0]))
    if game.secret[0] in game.player_thinks:
        print(str(game.secret[0]) + ' is not a unique product of any numbers between 1 and 9.')
        print('Continue guessing until you think you know the computer\'s secret number!')
        guess(game.guess_list)
    else:
        print(str(game.secret[0]) + ' is the product of ' + str(game.g_nums[0]) + ' x ' + str(game.g_nums[1]) + '.')
        print('You know the computer\'s secret number is: ' + str(sum(game.g_nums)) + '.')

initial_guess()
