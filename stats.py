
import os
from conllu import parse
import pandas as pd


def isverb(word):
    return word['upos'] == 'VERB'




def to_df(word):

    try:
        id=word['id']
    except:
        id=None
    try:   
        text= word['form']
    except:
        text=None
    try:
        lemma= word['lemma']
    except:
        lemma=None
    try:
        pos = word['upos']
    except:
        pos=None
    try:
        binyan= word['feats']['HebBinyan']
    except:
        binyan=None
    try:
        number= word['feats']['Number']
    except:
        number=None
    try:
        gender= word['feats']['Gender']
    except:
        gender=None
    try:
        person=word['feats']['Person']
    except:
        person=None
    try:
        tense= word['feats']['Tense']
    except:
        tense=None
    try:
        syntactic_attributes = word['deprel']
    except:
        syntactic_attributes=None
    
    data ={
        'id': id,
        'text': text,
        'lemma': lemma,
        'pos': pos,
        'binyan': binyan,
        'number': number,
        'gender': gender,
        'person': person,
        'tense': tense,
        'syntactic_attributes': syntactic_attributes
    }
    try:
        df = pd.DataFrame(data, index=[0])
    except:
        return pd.DataFrame()
    

    return df




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
        df = to_df(word)
        df_list.append(df)

combined_df = pd.concat([df for df in df_list], ignore_index=True)
verbs_df = combined_df[combined_df['pos'] == 'VERB']
combined_df.to_excel('wiki_words.xlsx', index=False)
verbs_df.to_excel('wiki_verbs.xlsx', index=False)

