from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

df = pd.read_csv('stories.csv', header=None).dropna().sample(n=5000)
df.columns = ['id', 'created_at', 'created_at_i', 'author', 'points', 'url_hostname', 'num_comments', 'title']
df = df[['created_at', 'points', 'url_hostname', 'title']]


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


def get_frequency(dataset, to_count, lower_limit=5, upper_limit=100):
    freq = pd.DataFrame(0, index=np.arange(len(clean_tokenized)), columns=unique_tokens)
    for i, item in enumerate(dataset):
        for token in item:
            if token in to_count:
                freq.iloc[i][token] += 1
    token_total = freq.sum(axis=0)
    freq = freq.loc[:, (token_total >= lower_limit) & (token_total <= upper_limit)]
    return freq


tokenized_headlines = [headline.split(' ') for headline in df['title']]

bad_chars = [',', ':', ';', '.', '"', "'", '’', '?', '/', '-', '+', '&', '(', ')']

clean_tokenized = cleanup(tokenized_headlines, bad_chars)

single_tokens, unique_tokens = find_unique(clean_tokenized)

counts = get_frequency(clean_tokenized, unique_tokens)

X_train, X_test, y_train, y_test = train_test_split(counts, df['points'], test_size=0.2, random_state=1)

clf = LinearRegression()
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
mse = sum((predictions - y_test) ** 2) / len(predictions)