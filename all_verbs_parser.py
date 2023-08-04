import os
import pandas as pd
import xml.etree.ElementTree as ET

directory = "tanach"
excel_folder = "excel"
filenames = [os.path.join(directory, f) for f in ["Exodus.xml", "Leviticus.xml", "Numbers.xml"]]
hebrew_binyans = ['NIFAL', 'PAAL', 'HIFIL', 'PIEL', 'PUAL', 'HITPAEL', 'HUFAL']
pos_values = ['ADVERB', 'PRONOUN', 'INTERROGATIVE', 'INTERJECTION', 'ADJECTIVE', 'CONJUNCTION', 'NEGATION',
              'PARTICIPLE', 'NOUN', 'PROPERNAME', 'VERB', 'PREPOSITION']
def all_words(filenames):
    data = []
    for filename in filenames:
        tree = ET.parse(filename)
        root = tree.getroot()
        for s in root.findall(".//s"):
            xml_id = s.get("{http://www.w3.org/XML/1998/namespace}id")
            for w in s.findall(".//w"):
                word = w.text
                lemma = w.get("lemma")
                for m in w.findall(".//m"):
                    phrase_id = m.get("phraseId")
                    ana = m.get("ana")
                    if ana:
                        pos_value = None
                        for pv in pos_values:
                            if f"#BASEFORM_POS_{pv}" in ana:
                                pos_value = pv
                                break
                        binyan_value = None
                        for bv in hebrew_binyans:
                            if f"#BASEFORM_BINYAN_{bv}" in ana:
                                binyan_value = bv
                                break
                        if pos_value or binyan_value:
                            row = {
                                "text": word,
                                "lemma": lemma,
                                "phrase id": phrase_id,
                                "xml id": xml_id,
                                "POS": pos_value,
                                "BINYAN": binyan_value
                            }
                            if row not in data:
                                data.append(row)

    df = pd.DataFrame(data)
    df.to_excel(os.path.join(excel_folder, 'tanach_words.xlsx'), index=False)

def all_verbs(filenames):
    data = []
    for filename in filenames:
        tree = ET.parse(filename)
        root = tree.getroot()
        for s in root.findall(".//s"):
            xml_id = s.get("{http://www.w3.org/XML/1998/namespace}id")
            for w in s.findall(".//w"):
                word = w.text
                lemma = w.get("lemma")
                for m in w.findall(".//m"):
                    phrase_id = m.get("phraseId")
                    ana = m.get("ana")
                    if ana and "#BASEFORM_POS_VERB" in ana:
                        for binyan in hebrew_binyans:
                            if f"#BASEFORM_BINYAN_{binyan}" in ana:
                                row = {
                                    "word": word,
                                    "lemma": lemma,
                                    "phraseid": phrase_id,
                                    "sentence id": xml_id,
                                    "BINYAN": binyan,
                                    "POS": 'VERB'
                                }
                                if row not in data:
                                    data.append(row)
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(excel_folder, 'tanach_verbs.xlsx'), index=False)

def pos_val(filenames):
    pos_values = set()
    for filename in filenames:
        tree = ET.parse(filename)
        root = tree.getroot()
        for m in root.findall(".//m"):
            ana = m.get("ana")
            if ana:
                for part in ana.split():
                    if part.startswith("#BASEFORM_POS_"):
                        pos_values.add(part.split("_")[-1])

    return list(pos_values)

def binyan_val(filenames):
    binyan_values = set()
    for filename in filenames:
        tree = ET.parse(filename)
        root = tree.getroot()
        for m in root.findall(".//m"):
            ana = m.get("ana")
            if ana:
                for part in ana.split():
                    if part.startswith("#BASEFORM_BINYAN_"):
                        binyan_values.add(part.split("_")[-1])

    binyan_list = list(binyan_values)
    return binyan_list


all_words(filenames)
all_verbs(filenames)
