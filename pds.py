import os
import pandas as pd

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element as Element
import re



WINDOW_SIZE = 2



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


excel_file_path = 'tagged_verbs.xlsx'
sheet_name = 'Tanach verbs'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)


grouped = df.groupby('source')

# Step 2: Access individual groups as separate DataFrames
list_of_dataframes = [group for _, group in grouped]
group_names = [name for name, _ in grouped]

df1 = list_of_dataframes[0]
row = df1.iloc[0]
path_to_file = os.path.join("tanach", "Exodus.xml")
tree = ET.parse(path_to_file)
root = tree.getroot()
words = get_sentence_words(row, root)
info = get_sentence_syntactic_info(row, root)
def baseform_filter(m):
    pattern = r"^ #BASEFORM"
    if m is not None:
        ana = m.get('ana')
        if ana is not None:
            if re.match(pattern, ana):
                return True
    return False


baseform_words = list(filter(baseform_filter, words))
print(len(baseform_words))
print(len(info))

#extract phrases into dict: key-phrase id, val-function
def dict_phrases(info):
    phrase_dict = {}
    for phrase in info:
        function = phrase.get('function')
        id = phrase.get('id')
        phrase_dict[id] = function
    return phrase_dict


print(dict_phrases(info))
print(len(dict_phrases(info)))
