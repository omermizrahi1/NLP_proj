import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element as Element
import pandas as pd
from verb import Verb
import os
from excel import write_dataframe_to_excel


def get_words(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    words = root.iter('w')
    return words


def get_verbs(words: tuple[Element, str]):
    verbs = []
    for word, src in words:
        if Verb.get_verb_info_xml(word) is not None:
            v = Verb(word, src)
            verbs.append(v)
    return verbs

def get_verbs_of_binayn(words, binyan):
    verbs = []
    for word, src in words:
        m = Verb.get_verb_info_xml(word)
        if m is not None:
            ana = m.get('ana')
            if binyan in ana:
                verbs.append(Verb(init_type='xml', word=word, src_file=src))
    return verbs



dirname = "tanach"
filenames = ["Exodus.xml",
             "Leviticus.xml",
             "Numbers.xml",]
binyan = 'NIFAL'
words = []
for filename in filenames:
    path_to_file = os.path.join(dirname, filename)
    file_words = [(x, path_to_file) for x in get_words(path_to_file)]
    words.extend(file_words)
nifal_words = get_verbs_of_binayn(words, binyan)


df_list = []
for v in nifal_words:
    if v.binyan == binyan:
        df = v.DataFrame()
        df_list.append(df)

combined_df = pd.concat([df for df in df_list], ignore_index=True)
print(combined_df)

file_path = 'nifal_tanach_verbs.xlsx'
sheet_name = 'Tanach verbs'
write_dataframe_to_excel(combined_df, sheet_name, file_path)




