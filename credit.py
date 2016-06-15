# Lending Club dataset for 2015 (https://resources.lendingclub.com/LoanStats3d.csv.zip)
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from matplotlib import pyplot as plt

# read the dataset
print('Reading CSV file and cleaning the dataset. \nThis will take ~40 seconds.\n')
df = pd.read_csv('lc/LoanStats3d.csv', skiprows=0, header=1, skipfooter=2)

# clean and prepare dataset for analysis

# drop any columns that do not describe credit risk or is a duplicate (ie: zip_code shows '##XXX' not '#####')
# emp_title is being dropped for now;  may come back later to tokenize and run machine learning algos
drop_list = ['id', 'member_id', 'url', 'desc', 'grade', 'pymnt_plan', 'zip_code', 'title', 'emp_title', 'policy_code',
             'initial_list_status', 'funded_amnt_inv', 'out_prncp_inv', 'total_pymnt_inv', 'recoveries', 'dti_joint',
             'collection_recovery_fee', 'funded_amnt', 'annual_inc_joint', 'application_type', 'mths_since_last_record',
             'verification_status_joint', 'last_pymnt_amnt', 'last_credit_pull_d', 'last_pymnt_d', 'next_pymnt_d',
             'mths_since_last_delinq', 'total_rec_late_fee', 'mths_since_last_major_derog',
             'collections_12_mths_ex_med']

for item in drop_list:
    df.drop(item, axis=1, inplace=True)

# convert employment length and tenor of loan to float values (would do int, but np.nan is float)
df['emp_length'] = df['emp_length'].replace('n/a', np.nan)
df['emp_length'] = df['emp_length'].replace({'\D': ''}, regex=True).astype('float64')
df['term'] = df['term'].replace({'\D': ''}, regex=True).astype('float64')

# convert interest rates from string to float
df['int_rate'] = df['int_rate'].str.rstrip('%').astype('float64') / 100

# very few records have home_ownership equal to 'ANY', so removing them from the dataset shouldn't be a problem
df = df[df['home_ownership'] != 'ANY']

# purpose_list contains less than 250 records -- move these to 'other'
purpose_list = ['educational', 'wedding', 'renewable_energy']
for item in purpose_list:
    df['purpose'] = df['purpose'].replace(purpose_list, 'other')

# adding 'purpose' columns to rename_dict would be tedious; will make its own dict and then use df.rename twice
purpose_dict = dict(zip(df['purpose'].unique(), 'purp_' + df['purpose'].unique()))

# values need to be lowercase; will be converted to columns after generating dummy values
# get dummy values for various columns, then add the new columns to the dataframe and remove old column
# lastly, rename the dummy value columns to something that references the column's origin
dummy_list = ['home_ownership', 'verification_status', 'loan_status', 'purpose']
for item in dummy_list:
    df[item] = df[item].str.lower()
    df = pd.concat([df, pd.get_dummies(df[item])], axis=1)
    df.drop(item, axis=1, inplace=True)

rename_dict = {'own': 'home_own',
               'mortgage': 'home_mort',
               'rent': 'home_rent',
               'not verified': 'verify_no',
               'source verified': 'verify_y1',
               'verified': 'verify_y2',
               'current': 'ls_current',
               'fully paid': 'ls_paid',
               'late (31-120 days)': 'ls_late_120',
               'late (16-30 days)': 'ls_late_30',
               'in grace period': 'ls_grace',
               'charged off': 'ls_chargeoff',
               'default': 'ls_default'}

df = df.rename(columns=rename_dict)
df = df.rename(columns=purpose_dict)

# identify good loans and bad loans (might include the 31 to 120 day late category later)
df.loc[df['ls_default'] == 1, 'bad_loan'] = 1
df.loc[df['ls_chargeoff'] == 1, 'bad_loan'] = 1
df.loc[df['bad_loan'] != 1, 'bad_loan'] = 0
df.loc[df['bad_loan'] != 1, 'good_loan'] = 1
df.loc[df['good_loan'] != 1, 'good_loan'] = 0

# add columns related to debt service and debt service coverage

# calculate annual debt service payments for Lending Club loans
df['annual_prin'] = sum([np.ppmt(df['int_rate'] / 12, i, df['term'], -df['loan_amnt'], 0) for i in range(1, 13)])
df['annual_prin'] = df['annual_prin'].round(2)
df['annual_int'] = sum([np.ipmt(df['int_rate'] / 12, i, df['term'], -df['loan_amnt'], 0) for i in range(1, 13)])
df['annual_int'] = df['annual_int'].round(2)
df['annual_debt_svc'] = df['annual_prin'] + df['annual_int']
df['annual_debt_svc'] = df['annual_debt_svc'].round(2)

# total revolving debt NOT attributable to Lending Club loans
df['other_rev_debt'] = df['total_bal_ex_mort'] - df['out_prncp']
df.loc[df['other_rev_debt'] < 0, 'other_rev_debt'] = 0

# total mortgage/installment debt (also not Lending Club)
df['other_mort_debt'] = df['tot_cur_bal'] - df['other_rev_debt']
df.loc[df['other_mort_debt'] < 0, 'other_mort_debt'] = 0

# estimated annual debt service requirement on non-Lending-Club revolving debt (at Lending Club int_rate, 5yr amort)
df['addl_annual_rev_ds'] = (12 * (df['other_rev_debt'] / 60)) + (df['int_rate'] * df['other_rev_debt'])
df['addl_annual_rev_ds'] = df['addl_annual_rev_ds'].round(2)

# estimated annual debt service requirement on non-Lending-Club term debt (at 1/2 Lending Club int_rate, 20yr amort)
df['addl_annual_mort_ds'] = (12 * (df['other_mort_debt'] / 240)) + ((df['int_rate'] / 2) * df['other_mort_debt'])
df['addl_annual_mort_ds'] = df['addl_annual_mort_ds'].round(2)

# total adjusted annual debt service on revolving debt
df['adj_annual_rev_ds'] = df['annual_debt_svc'] + df['addl_annual_rev_ds']

# total annual debt service on all debt
df['tot_adj_annual_ds'] = df['adj_annual_rev_ds'] + df['addl_annual_mort_ds']

# debt service coverage ratios for LC-only, all revolving debt, and total debt service (rounded to 2 decimal places)
df['dscr_lc'] = df['annual_inc'] / df['annual_debt_svc']
df['dscr_rev'] = df['annual_inc'] / df['adj_annual_rev_ds']
df['dscr_all'] = df['annual_inc'] / df['tot_adj_annual_ds']
df['dscr_lc'] = df['dscr_lc'].round(2)
df['dscr_rev'] = df['dscr_rev'].round(2)
df['dscr_all'] = df['dscr_all'].round(2)

# try to find something that closely approximates a FICO score -- will likely need to use random forests
# this regression is just a placeholder, so that I know where I left off at 3AM ...
logistic_model = LogisticRegression()
vars = ['term', 'delinq_2yrs', 'open_acc', 'pub_rec', 'chargeoff_within_12_mths', 'total_acc', 'tot_cur_bal',
        'num_accts_ever_120_pd', 'verify_no', 'tax_liens', 'home_own']
logistic_model.fit(df[vars], df['bad_loan'])
labels = logistic_model.predict(df[vars])
df['predicted_labels'] = labels
pred_probs = logistic_model.predict_proba(df[vars])
plt.scatter(df['total_acc'], pred_probs[:, 1])
