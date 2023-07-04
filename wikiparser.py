import os
from conllu import parse, parse_incr
from io import open
import pandas as pd
import openpyxl
from conllu.models import Token as Token
from verb import Verb
from openpyxl.utils.dataframe import dataframe_to_rows
from excel import write_dataframe_to_excel



dirname = "wiki"
filenames = [
                "iahltwiki_bagaz-mas-ribuy-dirot.conllu.txt",
                "iahltwiki_reparations-agreement.conllu.txt",
                "iahltwiki_psak-din-isascharov.conllu.txt",
                "iahltwiki_supreme-court.conllu.txt",
                "iahltwiki_mashber-menayot-habankim.conllu.txt",
                "iahltwiki_malve-kzar-moed.conllu.txt",
                "iahltwiki_shuk-hamaof.conllu.txt",
                "iahltwiki_british-mandate.conllu.txt",
                "iahltwiki_holy-sepulchre.conllu.txt"
                ]
sent_list = []  
for filename in filenames:
    path_to_file = os.path.join(dirname, filename)
    sentences = [(x, path_to_file) for x in parse(open(path_to_file, "r", encoding="utf-8").read())]
    sent_list.extend(sentences)


df_list = []
for sentence, src in sent_list:
    for word in sentence:
        if Verb.isverb_conllu(word):
            v = Verb(init_type='conllu', word=word, src_file=src, sentences=map(lambda x: x[0], sent_list))
            if v.binyan == 'NIFAL':
                df = v.DataFrame()
                df_list.append(df)
combined_df = pd.concat([df for df in df_list], ignore_index=True)
print(combined_df)

file_path = 'verbs.xlsx'
sheet_name = 'Wiki verbs'
file_exists = os.path.isfile(file_path)
write_dataframe_to_excel(combined_df, sheet_name, file_path)