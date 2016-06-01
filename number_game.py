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


def generate_numbers():
    return [random.randint(1, 9), random.randint(1, 9)]


def generate_matrix(who):
    if who == 1:
        matrix = np.arange(1, 10) * np.arange(1, 10).reshape(9, 1)
    elif who == 2:
        matrix = np.arange(1, 10) + np.arange(1, 10).reshape(9, 1)
    else:
        return np.zeros((9, 9), dtype=np.int)
    for i in range(9):
        for j in range(9):
            if i > j:
                matrix[i][j] = 0
    return matrix


def clear_unique(matrix):
    for i in range(9):
        for j in range(9):
            counter = 0
            c_list = []
            for k in range(9):
                for l in range(9):
                    if matrix[i][j] == matrix[k][l]:
                        counter += 1
            c_list.append(counter)
            if counter == 1:
                matrix[i][j] = 0
    return matrix


game_numbers = generate_numbers()

player_secret = game_numbers[0] * game_numbers[1]
player_matrix = generate_matrix(1)
player_thinks = clear_unique(player_matrix)

computer_secret = sum(game_numbers)
computer_matrix = generate_matrix(2)
computer_thinks = clear_unique(computer_matrix)

guess_list = []


def initial_guess():
    print('Your secret number is: ' + str(player_secret))
    if player_secret in player_thinks:
        print(str(player_secret) + ' is not a unique product of any numbers between 1 and 9.')
        print('Continue guessing until you think you know the computer\'s secret number!')
        guess(guess_list)
    else:
        print(str(player_secret) + ' is the product of ' + str(game_numbers[0]) + ' and ' + str(game_numbers[1]) + '.')
        print('You know the computer\'s secret number is: ' + str(sum(game_numbers)) + '.')


def possibilities(a):
    return [[i, int(a / i)] for i in range(1, 10) if a % i == 0 and a / i < 9 and i >= a / i]


def best_guesses(a):
    return [sum(possibilities(a)[i]) for i in range(len(possibilities(a)))]


def guess(g):
    if (len(g) + 1) % 2 != 0:
        g.append(input('Do you know the numbers? (y/n): '))
        if g[len(g) - 1] == 'y':
            final = input('Final guess: ')
            if int(final) == computer_secret:
                print('You win!')
            else:
                print('Nope, you lose! \nBetter luck next time! \nIt was actually ' + str(computer_secret))
        else:
            print('WE NEED TO FILTER HERE ... ')
    else:
        g.append('n')
        print('WE NEED TO FILTER HERE TOO ... ')
        guess(guess_list)


initial_guess()
