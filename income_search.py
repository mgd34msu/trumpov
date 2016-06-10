# Lending Club dataset for 2015 (https://resources.lendingclub.com/LoanStats3d.csv.zip)
import pandas as pd
from matplotlib import pyplot as plt


df = pd.read_csv('lc/LoanStats3d.csv', skiprows=0, header=1, skipfooter=2)
df = df[(df['emp_title'].notnull() == True) & (df["annual_inc"] > 0)]
cols = ['emp_title', 'emp_length', 'annual_inc', 'verification_status', 'addr_state']
df = df[cols]


def verified_income(dataframe):
    return dataframe[dataframe['verification_status'] == 'Verified']


def income_bounds(minimum, maximum, dataframe=df):
    return dataframe[(dataframe["annual_inc"] >= minimum) & (dataframe["annual_inc"] <= maximum)]


def job_search(job_title, dataframe=df):
    return dataframe[[job_title in str(dataframe['emp_title'].iloc[i]).lower() for i in range(len(dataframe))]]


df = job_search('financial', job_search('analyst'))
df = verified_income(df)
df = income_bounds(20000, 200000)

plt.title('Annual Income:  Financial Analyst')
plt.xlabel('Salary')
plt.ylabel('Reports')
plt.hist(df['annual_inc'], bins=18)
plt.show()
