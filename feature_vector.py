import pds
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np


verbs_df = pds.verbs_df
sentences_df = pds.combined_df
window_df = pds.window_df
window = pds.window
print(f'window: {window}')
encoder = OneHotEncoder()

feature_combinations = [
    ['lemma', 'binyan'],
    ['lemma'],
    ['lemma','binyan','number','gender'],
    ['binyan','number','gender'],
]

feature_combinations_for_window = [
    ['lemma', 'binyan'],
    ['lemma'],
    ['lemma','binyan','number','gender'],
    ['binyan','number','gender'],
]

# Create a list to store the resulting feature vectors
feature_vectors = []

# Iterate over the unique target word phrase ids in window_df
for phrase_id in window_df['target word phrase id'].unique():
    # Find all rows in window_df that have the same target word phrase id
    related_rows = window_df[window_df['target word phrase id'] == phrase_id]


# Iterate over the feature combinations
for features in feature_combinations:
    # Fit the encoder on the current feature combination
    encoder.fit(verbs_df[features])

    # Transform the features into a one-hot encoded representation
    one_hot = encoder.transform(verbs_df[features]).toarray()

    # Add the resulting feature vectors to the list
    feature_vectors.append(one_hot)

# Concatenate all the resulting feature vectors into a single array
X = np.hstack(feature_vectors)