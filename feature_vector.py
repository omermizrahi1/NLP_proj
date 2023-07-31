import pds
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np


verbs_df = pds.verbs_df
sentences_df = pds.combined_df
window_df = pds.window_df
encoder = OneHotEncoder()

feature_combinations = [
    ['lemma', 'binyan'],
    ['lemma'],
    ['lemma','binyan','number','gender'],
    ['binyan','number','gender'],
]

# Create a list to store the resulting feature vectors
feature_vectors = []

# Iterate over the feature combinations
for features in feature_combinations:
    # Fit the encoder on the current feature combination
    encoder.fit(verbs_df[features])

    # Transform the features into a one-hot encoded representation
    one_hot = encoder.transform(verbs_df[features]).toarray()

    # Add the resulting feature vectors to the list
    feature_vectors.append(one_hot)

# Concatenate all of the resulting feature vectors into a single array
X = np.hstack(feature_vectors)
