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


# Find the columns that contain the string 'target word phrase id'
cols_to_drop = [col for col in new_df.columns if 'target word phrase id' in col]

# Drop the columns from the DataFrame
new_df = new_df.drop(cols_to_drop, axis=1)
cols_to_drop = [col for col in new_df.columns if 'target word' in col and col != 'target word_0']
new_df = new_df.drop(cols_to_drop, axis=1)
new_df.to_excel('merged.xlsx', index=False)



# למה + מורפולוגי
# למה + תחבירי
# למה + מורפולוגי + תחבירי
# למה + חלק דיבר
# מורפולוגי + תחבירי
# חלק דיבר + תחבירי
# feature_vectors = []
# feature_combinations = []
# for i in range(2*window + 1):
#     feature_combinations += [
#         [f'POS_{i}', f'NUMBER_{i}'],
#         [f'POS_{i}',f'TENSE_{i}',f'FUNCTION_{i}'],
#         [f'STATUS_{i}',f'FUNCTION_{i}',f'BINYAN{i}'],
#         [f'TENSE_{i}',f'NUMBER_{i}',f'FUNCTION_{i}'],
#         [f'POS_{i}',f'NUMBER_{i}',f'STATUS_{i}',f'FUNCTION_{i}',f'BINYAN{i}'],
#         [f'POS_{i}',f'NUMBER_{i}',f'STATUS_{i}',f'FUNCTION_{i}',f'BINYAN{i}',f'TENSE_{i}'],
#     ]


# print(feature_combinations)
# # # Create a list to store the resulting feature vectors

# # # Iterate over the feature combinations
# for features in feature_combinations:
#         # Fit the encoder on the current feature combination
#     encoder.fit(new_df[features])

#         # Transform the features into a one-hot encoded representation
#     one_hot = encoder.transform(new_df[features]).toarray()

#         # Add the resulting feature vectors to the list
#     feature_vectors.append(one_hot)

# # Concatenate all the resulting feature vectors into a single array
# X = np.hstack(feature_vectors)

