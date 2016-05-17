import numpy as np
import random

vector_a = np.ndarray([9, 1])
vector_b = np.ndarray([1, 9])
clue_prod_matrix = np.ndarray([9, 9])
clue_sums_matrix = np.ndarray([9, 9])
filter_no_unique = np.ndarray([9, 9])
filter_is_unique = np.ndarray([9, 9])

for i in range(9):
    vector_a[i] = i + 1
    vector_b[0][i] = i + 1

matrix_a = vector_a * vector_b
matrix_b = vector_a + vector_b

number_a = random.randrange(1,9)
number_b = random.randrange(1,9)

clue_prd = int(number_a) * int(number_b)
clue_sum = int(number_a) + int(number_b)


def m_filter(a):
    for y in range(9):
        for z in range(9):
            if np.count_nonzero(a != a[y][z]) == 80:
                filter_no_unique[y][z] = 0
            elif a[y][z] == 0:
                filter_no_unique[y][z] = 0
            else:
                filter_no_unique[y][z] = 1
    return filter_no_unique


for i in range(9):
    for j in range(9):
        if i > j:
            matrix_a[i][j] = 0
            matrix_b[i][j] = 0

for i in range(9):
    for j in range(9):
        if np.count_nonzero(matrix_a != matrix_a[i][j]) == 80:
            filter_no_unique[i][j] = 0
            filter_is_unique[i][j] = 1
        elif matrix_a[i][j] == 0:
            filter_no_unique[i][j] = 0
            filter_is_unique[i][j] = 0
        else:
            filter_no_unique[i][j] = 1
            filter_is_unique[i][j] = 0

for i in range(9):
    for j in range(9):
        if matrix_a[i][j] == clue_prd:
            clue_prod_matrix[i][j] = matrix_a[i][j]
        else:
            clue_prod_matrix[i][j] = 0
        if matrix_b[i][j] == clue_sum:
            clue_sums_matrix[i][j] = matrix_b[i][j]
        else:
            clue_sums_matrix[i][j] = 0

guess_list = []


def guess(g=guess_list):
    if np.fmod((len(g) + 1), 2) != 0:
        guess_list.append(input('Do you know the numbers? (y/n): '))
        if g[len(g) - 1] == 'y':
            final = input('Final guess: ')
            if int(final) == clue_prd:
                print('You win!')
                return 0
            else:
                print('Nope, you lose!  Better luck next time!')
                print('It was actually ' + str(clue_prd))
                return 0
        else:
            m_filter(matrix_a * filter_no_unique)
    else:
        guess_list.append('n')
        m_filter(matrix_b * filter_no_unique)
        guess()
    if np.count_nonzero(clue_prod_matrix * filter_no_unique) == 1:
        print('Computer has won.')
        sum_num = np.argwhere(clue_prod_matrix * filter_no_unique != 0)[0]
        your_num = sum_num[0] + sum_num[1] + 2
        print('Your number was: ' + str(your_num))
        return 0
    show_matrix()


def show_matrix():
    print(clue_sums_matrix * filter_no_unique)

print('Your secret number is: ' + str(clue_sum))
show_matrix()
guess()