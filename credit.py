# Lending Club dataset for 2015 (https://resources.lendingclub.com/LoanStats3d.csv.zip)
import pandas as pd
# from matplotlib import pyplot as plt

# read the dataset
df = pd.read_csv('lc/LoanStats3d.csv', skiprows=0, header=1, skipfooter=2)

# clean and prepare dataset for analysis
drop_list = ['id', 'member_id', 'url', 'desc', 'mths_since_last_record', 'pymnt_plan', 'zip_code',
             'initial_list_status', 'funded_amnt_inv', 'out_prncp_inv', 'total_pymnt_inv', 'policy_code',
             'recoveries', 'collection_recovery_fee']

for item in drop_list:
    df.drop(item, axis=1, inplace=True)

# this is very inefficient -- need to redo with regex
df['emp_length'] = df['emp_length'].replace('n/a', 0)
df['emp_length'] = df['emp_length'].replace('< 1 year', 0)
df['emp_length'] = df['emp_length'].replace('1 year', 1)
df['emp_length'] = df['emp_length'].replace('2 years', 2)
df['emp_length'] = df['emp_length'].replace('3 years', 3)
df['emp_length'] = df['emp_length'].replace('4 years', 4)
df['emp_length'] = df['emp_length'].replace('5 years', 5)
df['emp_length'] = df['emp_length'].replace('6 years', 6)
df['emp_length'] = df['emp_length'].replace('7 years', 7)
df['emp_length'] = df['emp_length'].replace('8 years', 8)
df['emp_length'] = df['emp_length'].replace('9 years', 9)
df['emp_length'] = df['emp_length'].replace('10+ years', 10)

# same goes for these two lines -- need to make more efficient
df['term'] = df['term'].replace(' 36 months', 36)
df['term'] = df['term'].replace(' 60 months', 60)

df = df[df['home_ownership'] != 'ANY']

# get dummy values for home_ownership column
pd.concat([df, pd.get_dummies(df['home_ownership'])], axis=1)


