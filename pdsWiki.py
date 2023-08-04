import os
import pandas as pd
def get_window(words, index, window_size):
    start = max(0, index - window_size)
    end = min(len(words), index + window_size + 1)

    while len(words.loc[(words['index'] >= start) & (words['index'] < index)]) < window_size and start > 0:
        start -= 1
        
    max_index = words['index'].max()
    while len(words.loc[(words['index'] > index) & (words['index'] < end)]) < window_size and end < max_index:
        end += 1
    
    window = words.loc[(words['index'] >= start) & (words['index'] < end)]
    return window

def get_words_by_window(sentences_df, verbs_df, window_size=2):
    df_list = []
    for _, verb_row in verbs_df.iterrows():
        print(verb_row)
        verb = verb_row['text'] 
        sentence_id = verb_row['sentence id']
        index = verb_row['index']
        sentence_row = sentences_df.loc[sentences_df['sentence id'] == sentence_id]
        related_rows = sentence_row[sentence_row['target verb'] == verb]
        window = get_window(related_rows, index, window_size=window_size)
        window_df = pd.DataFrame({
            'target word': verb,
            'target word index': index,
            'POS': window['POS'],
            'GENDER': window['GENDER'],
            'NUMBER': window['NUMBER'],
            'LEMMA': window['lemma'],
            'SYNTACTIC ATTRIBUTES': window['syntactic attributes'],
            'PERSON': window['person'],
            'TENSE': window['tense'],
            'BINYAN': window['binyan'],
            'SENTENCE ID': window['sentence id']
        })
        df_list.append(window_df)
    result_df = pd.concat(df_list, ignore_index=True)
    return result_df

excel_file_path = 'verbs.xlsx'
sheet_name = 'Wiki verbs'
verbs_df = pd.read_excel(os.path.join('excel', excel_file_path), sheet_name=sheet_name)
print(verbs_df)

grouped = verbs_df.groupby('source')
list_of_dataframes = [group for _, group in grouped]
sources = [name for name, _ in grouped]

combined_df = pd.read_excel(os.path.join('excel', 'sentences.xlsx'))


# Set window size and generate a dataframe of words in the window around each target verb
window = 5
window_df = get_words_by_window(combined_df,verbs_df,window)
window_df.to_excel(os.path.join('excel', f'window_words_{window}.xlsx'), index=False)

    