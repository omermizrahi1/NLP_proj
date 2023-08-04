
import os
import pdsWiki
import pandas as pd


sheet_name = 'Wiki verbs'
verbs_df = pdsWiki.verbs_df
sentences_df = pdsWiki.combined_df
window_df = pdsWiki.window_df
window = pdsWiki.window
print(f'window: {window}')



# Split the 'SENTENCE ID' column into a prefix (all the parts before the last hyphen)
# and a suffix (the part after the last hyphen)
window_df[['SENTENCE ID Text', 'SENTENCE ID Number']] = window_df['SENTENCE ID'].str.rsplit('-', n=1, expand=True)

# Convert the suffix to integers for correct sorting
window_df['SENTENCE ID Number'] = window_df['SENTENCE ID Number'].astype(int)

# Sort by the numerical part of 'SENTENCE ID' and 'target word index'
window_df = window_df.sort_values(['SENTENCE ID Text', 'SENTENCE ID Number', 'target word index'])

# Now group by the original 'SENTENCE ID' column and 'target word index'
grouped = window_df.groupby(['SENTENCE ID', 'target word index'])

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
cols_to_drop = [col for col in new_df.columns if 'target word index' in col]

# Drop the columns from the DataFrame
new_df = new_df.drop(cols_to_drop, axis=1)
cols_to_drop = [col for col in new_df.columns if 'target word' in col and col != 'target word_0']

new_df = new_df.drop(cols_to_drop, axis=1)


comb_df = new_df.copy()

# Create the combinations of features for each i value
for i in range(5):
    comb_df[f'lemma_morphological_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'GENDER_{i}'] + '' + comb_df[f'NUMBER_{i}'] + '' + comb_df[f'BINYAN_{i}']
    # df[f'lemma_syntactic_{i}'] = df[f'target word_{i}'] + '' + df[f'function_{i}']
    comb_df[f'lemma_morphological_syntactic_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'GENDER_{i}'] + '' + comb_df[f'NUMBER_{i}'] + '' + comb_df[f'BINYAN_{i}'] + '' + comb_df[f'SYNTACTIC ATTRIBUTES_{i}']
    # df[f'lemma_part_of_speech_{i}'] = df[f'target word_{i}'] + '' + df[f'POS_{i}']
    comb_df[f'morphological_syntactic_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'GENDER_{i}'] + '' + comb_df[f'NUMBER_{i}'] + '' + comb_df[f'BINYAN_{i}'] + '' + comb_df[f'SYNTACTIC ATTRIBUTES_{i}']
    comb_df[f'part_of_speech_syntactic_{i}'] = comb_df[f'POS_{i}'] + '' + comb_df[f'SYNTACTIC ATTRIBUTES_{i}']

# Create a list of the feature combination columns
feature_combination_columns = [f'{col}_{i}' for col in ['lemma_morphological','lemma_morphological_syntactic', 'morphological_syntactic', 'part_of_speech_syntactic'] for i in range(5)]




new_df_glinert = new_df.copy()
new_df_blau = new_df.copy()
comb_df_glinert = comb_df.copy()
comb_df_blau = comb_df.copy()

tagged_verbs = pd.read_excel(os.path.join('excel', 'tagged_verbs.xlsx'), sheet_name=sheet_name)
glinert_column = tagged_verbs['Glinert']
blau_column = tagged_verbs['Blau']

new_df_glinert = pd.concat([new_df_glinert, glinert_column], axis=1)
new_df_blau = pd.concat([new_df_blau, blau_column], axis=1)
comb_df_glinert = pd.concat([comb_df_glinert, glinert_column], axis=1)
comb_df_blau = pd.concat([comb_df_blau, blau_column], axis=1)

# First sort the dataframe by 'SENTENCE ID Text_0' and 'SENTENCE ID Number_0'
new_df = new_df.sort_values(by=['SENTENCE ID Text_0', 'SENTENCE ID Number_0'])

# Now drop the unnecessary columns
for i in range(11):
    new_df = new_df.drop(columns=[f'SENTENCE ID Text_{i}', f'SENTENCE ID Number_{i}'], errors='ignore')

# Repeat the same process for other dataframes
new_df_glinert = new_df_glinert.sort_values(by=['SENTENCE ID Text_0', 'SENTENCE ID Number_0'])
for i in range(11):
    new_df_glinert = new_df_glinert.drop(columns=[f'SENTENCE ID Text_{i}', f'SENTENCE ID Number_{i}'], errors='ignore')

new_df_blau = new_df_blau.sort_values(by=['SENTENCE ID Text_0', 'SENTENCE ID Number_0'])
for i in range(11):
    new_df_blau = new_df_blau.drop(columns=[f'SENTENCE ID Text_{i}', f'SENTENCE ID Number_{i}'], errors='ignore')

comb_df_glinert = comb_df_glinert.sort_values(by=['SENTENCE ID Text_0', 'SENTENCE ID Number_0'])
for i in range(11):
    comb_df_glinert = comb_df_glinert.drop(columns=[f'SENTENCE ID Text_{i}', f'SENTENCE ID Number_{i}'], errors='ignore')

comb_df_blau = comb_df_blau.sort_values(by=['SENTENCE ID Text_0', 'SENTENCE ID Number_0'])
for i in range(11):
    comb_df_blau = comb_df_blau.drop(columns=[f'SENTENCE ID Text_{i}', f'SENTENCE ID Number_{i}'], errors='ignore')


new_df.to_excel(os.path.join('excel', 'merged.xlsx'), index=False)
new_df_glinert.to_excel(os.path.join('excel', 'merged_glinert.xlsx'), index=False)
new_df_blau.to_excel(os.path.join('excel', 'merged_blau.xlsx'), index=False)
comb_df_glinert.to_excel(os.path.join('excel', 'merged_comb_glinert.xlsx'), index=False)
comb_df_blau.to_excel(os.path.join('excel', 'merged_comb_blau.xlsx'), index=False)