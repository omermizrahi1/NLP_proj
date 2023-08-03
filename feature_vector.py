import pds
import pandas as pd


sheet_name = 'Tanach verbs'
verbs_df = pds.verbs_df
sentences_df = pds.combined_df
window_df = pds.window_df
window = pds.window
print(f'window: {window}')



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


comb_df = new_df

# Create the combinations of features for each i value
for i in range(5):
    comb_df[f'lemma_morphological_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'GENDER_{i}'] + '' + comb_df[f'NUMBER_{i}'] + '' + comb_df[f'STATUS_{i}']
    # df[f'lemma_syntactic_{i}'] = df[f'target word_{i}'] + '' + df[f'function_{i}']
    comb_df[f'lemma_morphological_syntactic_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'GENDER_{i}'] + '' + comb_df[f'NUMBER_{i}'] + '' + comb_df[f'STATUS_{i}'] + '' + comb_df[f'function_{i}']
    # df[f'lemma_part_of_speech_{i}'] = df[f'target word_{i}'] + '' + df[f'POS_{i}']
    comb_df[f'morphological_syntactic_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'GENDER_{i}'] + '' + comb_df[f'NUMBER_{i}'] + '' + comb_df[f'STATUS_{i}'] + '' + comb_df[f'function_{i}']
    comb_df[f'part_of_speech_syntactic_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'function_{i}']

# Create a list of the feature combination columns
feature_combination_columns = [f'{col}_{i}' for col in ['lemma_morphological','lemma_morphological_syntactic', 'morphological_syntactic', 'part_of_speech_syntactic'] for i in range(5)]


new_df_glinert = new_df.copy()
new_df_blau = new_df.copy()
comb_df_glinert = comb_df.copy()
comb_df_blau = comb_df.copy()

tagged_verbs = pd.read_excel('tagged_verbs.xlsx', sheet_name=sheet_name)
glinert_column = tagged_verbs['Glinert']
blau_column = tagged_verbs['Blau']

new_df_glinert = pd.concat([new_df_glinert, glinert_column], axis=1)
new_df_blau = pd.concat([new_df_blau, blau_column], axis=1)
comb_df_glinert = pd.concat([comb_df_glinert, glinert_column], axis=1)
comb_df_blau = pd.concat([comb_df_blau, blau_column], axis=1)

new_df.to_excel('merged.xlsx', index=False)
new_df_glinert.to_excel('merged_glinert.xlsx', index=False)
new_df_blau.to_excel('merged_blau.xlsx', index=False)
comb_df_glinert.to_excel('merged_comb_glinert.xlsx', index=False)
comb_df_blau.to_excel('merged_comb_blau.xlsx', index=False)

