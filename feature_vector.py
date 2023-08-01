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



# Group the rows by 'target word phrase id'
grouped = window_df.groupby('target word phrase id')

# Create a new DataFrame to store the concatenated rows
new_df = pd.DataFrame()

# Iterate over each group
for name, group in grouped:
    # Create a new row to store the concatenated values
    new_row = {}
    # Iterate over each row in the group, using an independent index 'i' in the range [0, 2*window]
    for i, (index, row) in enumerate(group.iterrows()):
        if i > 2 * window:
            break
        # Iterate over each column in the row
        for col in row.index:
            # Concatenate the value to the new row, using the independent index 'i' as a suffix for the column name
            new_row[f'{col}_{i}'] = row[col]
    # Append the new row to the new DataFrame
    new_df = new_df.append(new_row, ignore_index=True)

# Reorder the columns to match the desired order
new_df = new_df[[f'{col}_{i}' for i in range(2*window+1) for col in window_df.columns]]


new_df.to_excel('merged.xlsx', index=False)


# feature_combinations = [
#     ['lemma', 'binyan'],
#     ['lemma'],
#     ['lemma','binyan','number','gender'],
#     ['binyan','number','gender'],
# ]
#
# feature_combinations_for_window = [
#     ['lemma', 'binyan'],
#     ['lemma'],
#     ['lemma','binyan','number','gender'],
#     ['binyan','number','gender'],
# ]
#
# # Create a list to store the resulting feature vectors
# feature_vectors = []
#
# # Iterate over the unique target word phrase ids in window_df
# for phrase_id in window_df['target word phrase id'].unique():
#     # Find all rows in window_df that have the same target word phrase id
#     related_rows = window_df[window_df['target word phrase id'] == phrase_id]
#
#
# # Iterate over the feature combinations
# for features in feature_combinations:
#     # Fit the encoder on the current feature combination
#     encoder.fit(verbs_df[features])
#
#     # Transform the features into a one-hot encoded representation
#     one_hot = encoder.transform(verbs_df[features]).toarray()
#
#     # Add the resulting feature vectors to the list
#     feature_vectors.append(one_hot)
#
# # Concatenate all the resulting feature vectors into a single array
# X = np.hstack(feature_vectors)