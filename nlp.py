# predicts upvotes based on words in Hacker News headline

from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

# stories.csv is ~150MB so not uploading that to github (is actually already available -- see readme
# drop any rows with missing data, then take a random sample of 5000
df = pd.read_csv('stories.csv', header=None).dropna().sample(n=5000)
df.columns = ['id', 'created_at', 'created_at_i', 'author', 'points', 'url_hostname', 'num_comments', 'title']
df = df[['created_at', 'points', 'url_hostname', 'title']]


# start cleanup of dataset by making everything lowercase and then removing punctuation, etc, and tokenizing words
def cleanup(dataset, to_clear):
    cleaned = []
    for item in dataset:
        tokens = []
        for token in item:
            token = token.lower()
            for char in to_clear:
                if char in token:
                    token = token.replace(char, '')
            tokens.append(token)
        cleaned.append(tokens)
    return cleaned


# grabs unique tokens, and filters them from any unique tokens that were used only one time
def find_unique(dataset):
    single = []
    unique = []
    for item in dataset:
        for token in item:
            if token not in single:
                single.append(token)
            elif token in single and token not in unique:
                unique.append(token)
    return single, unique


# filters out tokens used less or more than upper & lower bounds; finds frequency of use of remaining tokens
def get_frequency(dataset, to_count, lower_limit=5, upper_limit=100):
    freq = pd.DataFrame(0, index=np.arange(len(clean_tokenized)), columns=unique_tokens)
    for i, item in enumerate(dataset):
        for token in item:
            if token in to_count:
                freq.iloc[i][token] += 1
    token_total = freq.sum(axis=0)
    freq = freq.loc[:, (token_total >= lower_limit) & (token_total <= upper_limit)]
    return freq


# make a list of tokens from the 'title' column of the dataframe ( dataset argument of cleanup() )
tokenized_headlines = [headline.split(' ') for headline in df['title']]

# these are the characters we want to eliminate ( to_clean argument of cleanup() )
bad_chars = [',', ':', ';', '.', '"', "'", '’', '?', '/', '-', '+', '&', '(', ')']

# output of two previously defined variables when passed through cleanup()
clean_tokenized = cleanup(tokenized_headlines, bad_chars)

# split the tokens based on one-time or multiple-time usage
single_tokens, unique_tokens = find_unique(clean_tokenized)

# frequency of token usage for each token (limited by default min/max args -- see function for details)
counts = get_frequency(clean_tokenized, unique_tokens)

# time to do some regression analysis
# generate training and test sets
X_train, X_test, y_train, y_test = train_test_split(counts, df['points'], test_size=0.2, random_state=1)
clf = LinearRegression()

# train the model
clf.fit(X_train, y_train)

# make predictions with the test set, based on trained linear regression model
predictions = clf.predict(X_test)

# check the variance
mse = sum((predictions - y_test) ** 2) / len(predictions)

# compare model output to dataset ... likely very poor
print('Mean (df["points"]): ' + str(df['points'].mean()) + '\n')
print('RMSE: ' + str(mse**(1/2)))
print('Std Dev: ' + str(df['points'].std()) + '\n')
if mse**(1/2) > df['points'].std():
    print('Root Mean Squared Error > Standard Deviation')

# will look at using random forests to get a better result
