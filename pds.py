import os
import pandas as pd
from conll_df import conll_df
from bs4 import BeautifulSoup
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


def baseform_filter(m):
    pattern = r"^ #BASEFORM"
    if m is not None:
        ana = m.get('ana')
        if ana is not None:
            if re.match(pattern, ana):
                return True
    return False


def extract_BASEFORM_X_Y(input_string):
    # Define the regex pattern to match "BASEFORM_" followed by X and Y
    pattern = r"BASEFORM_([A-Z]+)_([A-Z]+)"
    matches = re.findall(pattern, input_string)
    extracted_values = {}
    for match in matches:
        x_value, y_value = match
        extracted_values[x_value] = y_value

    return extracted_values


# read the excel file
excel_file_path = 'tagged_verbs.xlsx'
sheet_name = 'Tanach verbs'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name)

# group the dataframe by source
grouped = df.groupby('source')
list_of_dataframes = [group for _, group in grouped]
sources = [name for name, _ in grouped]


for df,source in zip(list_of_dataframes, sources):
    for index, row in df.iterrows():
        path_to_file = os.path.join("tanach", source)
        tree = ET.parse(path_to_file)
        root = tree.getroot()
        words = get_sentence_words(row, root)
        info = get_sentence_syntactic_info(row, root)
        baseform_words = list(filter(baseform_filter, words))
        print(len(baseform_words))
        print(len(info))
        for word in baseform_words:
            w = extract_BASEFORM_X_Y(baseform_words[0].get('ana'))
            w['phraseId'] = word.get('phraseId')
