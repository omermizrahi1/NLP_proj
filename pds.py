import os
import pandas as pd
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element as Element
import re




def get_sentence_words(df_row, root):
    xml_namespace = "{http://www.w3.org/XML/1998/namespace}" 
    sentence_id = df_row['sentence id']
    sentence = root.iter('s')
    for s in sentence:
        if s.get(f'{xml_namespace}id') == sentence_id:
            ms = list(s.iter('m'))
            return ms
    return None


def get_sentence_syntactic_info(df_row, root):
    xml_namespace = "{http://www.w3.org/XML/1998/namespace}" 
    sentence_id = df_row['sentence id']
    sentence = root.iter('s')
    for s in sentence:
        if s.get(f'{xml_namespace}id') == sentence_id:
            phrases = list(s.iter('phrase'))
            return phrases       
    return None


def baseform_filter(m):
    pattern = r"^ #BASEFORM"
    if m is not None:
        ana = m.get('ana')
        if ana is not None:
            if re.match(pattern, ana):
                return True
    return False


#extract phrases into dict: key-phrase id, val-function
def dict_phrases(info):
    phrase_dict = {}
    for phrase in info:
        function = phrase.get('function')
        id = phrase.get('id')
        phrase_dict[id] = function
    return phrase_dict




def extract_BASEFORM_X_Y(input_string):
    # Define the regex pattern to match "BASEFORM_" followed by X and Y
    pattern = r"BASEFORM_([A-Z0-9]+)_([A-Z0-9]+)"
    matches = re.findall(pattern, input_string)
    extracted_values = {}
    for match in matches:
        x_value, y_value = match
        extracted_values[x_value] = y_value

    return extracted_values

def dict_morpholical(word):
    w = extract_BASEFORM_X_Y(word.get('ana'))
    w['phrase id'] = word.get('phraseId')
    w['text'] = word.text
    return w



def dict_word(word, info, sentence_id, target_verb):
    w = dict_morpholical(word)
    phrase_dict = dict_phrases(info)
    phrase_id = w['phrase id']
    w['function'] = phrase_dict[phrase_id]
    w['sentence id'] = sentence_id
    w['target verb'] = target_verb
    return w



# read the excel file
excel_file_path = 'nifal_tanach_verbs.xlsx'
sheet_name = 'Tanach verbs'
verbs_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
grouped = verbs_df.groupby('source')
list_of_dataframes = [group for _, group in grouped]
sources = [name for name, _ in grouped]
if os.path.exists("sentences.xlsx"):
    df_list = []
    for verbs_df,source in zip(list_of_dataframes, sources):
        path_to_file = os.path.join("tanach", source)
        tree = ET.parse(path_to_file)
        root = tree.getroot()
        for index, row in verbs_df.iterrows():
            words = get_sentence_words(row, root)
            info = get_sentence_syntactic_info(row, root)
            baseform_words = list(filter(baseform_filter, words))
            for i, word  in enumerate(baseform_words):
                w = dict_word(word, info, row['sentence id'], row['text'])
                w['index'] = i
                df_list.append(pd.DataFrame(w, index=[0]))
    combined_df = pd.concat([df for df in df_list], ignore_index=True)
    combined_df.to_excel('sentences.xlsx', index=False)
else:
    combined_df = pd.read_excel('sentences.xlsx')

excel_file_path = 'nifal_tanach_verbs.xlsx'
sheet_name = 'Tanach verbs'
verbs_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
def get_window(words, index, window_size):
    start = max(0, index - window_size)
    end = min(len(words), index + window_size + 1)
    return words[start:end]

# Loop through the rows of the verbs DataFrame
def get_words_by_window(sentences_df,verbs_df,window_size=2):
    df_list = []
    for _, verb_row in verbs_df.iterrows():
        verb = verb_row['text']
        phrase_id = verb_row['phrase id']
        sentence_row = sentences_df.loc[sentences_df['phrase id'] == phrase_id]
        index = sentence_row['index'].values[0]
        # Find all rows in sentences_df that have a target verb value equal to verb by masking
        related_rows = sentences_df[combined_df['target verb'] == verb]
        window = get_window(related_rows,index,window_size=window_size)
        window_df = pd.DataFrame({
            'target word': verb,
            'target word phrase id': phrase_id,
            'POS': window['POS'],
            'GENDER': window['GENDER'],
            'NUMBER': window['NUMBER'],
            'STATUS': window['STATUS'],
            'function': window['function'],
            'PERSON': window['PERSON'],
            'TENSE': window['TENSE'],
            'BINYAN': window['BINYAN']
        })
        df_list.append(window_df)

    result_df = pd.concat(df_list, ignore_index=True)
    return result_df

window = 5
window_df = get_words_by_window(combined_df,verbs_df,window)
window_df.to_excel(f'window_words_{window}.xlsx', index=False)

