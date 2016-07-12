import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


class Student:
    '''student class -- id starts at 10001, then autoincrements'''
    next_id = itertools.count(10001)

    def __init__(self, name, grade):
        '''increments id, then take name and grade'''
        self.id = next(Student.next_id)
        self.name = name
        self.grade = grade

students = pd.DataFrame(columns=['id', 'name', 'grade'])
students['id'] = students['id'].astype(int)
students['grade'] = students['grade'].astype(int)


def add_students(n, df=students):
    start = df.shape[0]
    for i in range(n):
        s = Student(input('name: '), input('grade: '))
        df.loc[start + i] = int(s.id), str(s.name), int(s.grade)

# names and grades to populate a dataframe -- so we don't have to enter a lot of info manually for testing
names = ['Adam', 'Bill', 'Chris', 'Dave', 'Edward', 'Fred', 'George', 'Holly', 'Ida', 'Jenn', 'Kate', 'Liz', 'Molly',
         'Nancy', 'Arlene', 'Betty', 'Cindy', 'Debby', 'Elizabeth', 'Francine', 'Gwen', 'Hank', 'Ike', 'Jeff', 'Kyle',
         'Lenny', 'Mike', 'Ned', 'Alex', 'Anne', 'Bart', 'Beth', 'Carl', 'Connie', 'Dan', 'Denice', 'Earl', 'Emily',
         'Francis', 'Farrah', 'Guy', 'Gabby']

# Population will be 10000 students (or uncomment next line, and delete the one after it to make a custom pop. size)
# size = input('Number of students to generate: ')
size = 10000

for i in range(int(size)):
    s = Student(names[random.randint(0, len(names) - 1)], random.randint(1, 100))
    students.loc[i] = int(s.id), str(s.name), int(s.grade)

# population mean and standard deviation -- of 'grade' column
pop_mean = students['grade'].mean()
pop_stdev = students['grade'].std()


def get_sample(df, size):
    '''grab a sample, also get mean and standard dev'''
    sample_df = df.sample(size)
    x_bar = sample_df['grade'].mean()
    stdev = sample_df['grade'].std()
    return sample_df, x_bar, stdev


def get_zscore(df):
    '''calculate the z-score'''
    return [(x - x_bar) / stdev for x in df['grade']]

sample_df, x_bar, stdev = get_sample(students, 100)

sample_df.insert(3, 'z_score', get_zscore(sample_df))

# sample_df histogram
plt.hist(sample_df['z_score'])
