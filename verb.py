
import os
from conllu import parse
from conllu.models import Token as Token
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element as Element
import re
import pandas as pd




class Verb:
    def __init__(self, init_type: str, word, src_file: str, sentences = None):
        if init_type == "conllu":
            self.conllu_init(word, src_file, sentences)
        elif init_type == "xml":
            self.xmlinit(word, src_file)
        else:
            raise ValueError("Invalid init_type")
        
    ###  CONLLU  ###
    def conllu_init(self, word: Token, src_file: str, sentences):
        if sentences is None:
            raise ValueError("sentences is None")
        if not self.isverb_conllu(word):
            raise ValueError("Word is not a verb")
        self.phrase_id = word['id']
        self.lemma = word['lemma']
        self.text = word['form']
        try:
            self.gender = word['feats']['Gender']
        except: 
            self.gender = None
        try:    
            self.number = word['feats']['Number']
        except:
            self.number = None
        try:
            self.person = word['feats']['Person']
        except:
            self.person = None
        try:
            self.tense = word['feats']['Tense']
        except:
            self.tense = None
        try:
            self.binyan = word['feats']['HebBinyan']
        except:
            self.binyan = None
        try:
            self.syntactic_attributes = word['deprel']
        except:
            self.syntactic_attributes = None


        self.source = os.path.basename(src_file)
        self.sentence = None
        sentences = parse(open(src_file, "r", encoding="utf-8").read())
        for sentence in sentences:
            if self.sentence is not None:
                break
            for w in sentence:
                if w['id'] == self.phrase_id and w['form'] == self.text:
                    self.sentence = sentence.metadata['sent_id']
            
        
    ### XML ###
    def xmlinit(self, word: Element, src_file: str):
        root = ET.parse(src_file).getroot()
        m = self.get_verb_info_xml(word)
        if m is None:
            raise("Error: word is not a verb")
        ana = m.get('ana')
            
        self.source = os.path.basename(src_file) 
        self.phrase_id = m.get('phraseId')
        self.lemma = word.get('lemma')
        self.text = word.text
        self.root  = word.get('root')
        try:
            self.gender = re.search(r'#BASEFORM_GENDER_(\w+)', ana).group(1)
        except AttributeError:
            self.gender = None

        try:
            self.number = re.search(r'#BASEFORM_NUMBER_(\w+)', ana).group(1)
        except AttributeError:
            self.number = None

        try:
            self.person = re.search(r'#BASEFORM_PERSON_(\w+)', ana).group(1)
        except AttributeError:
            self.person = None

        try:
            self.tense = re.search(r'#BASEFORM_TENSE_(\w+)', ana).group(1)
        except AttributeError:
            if "#BASEFORM_POS_PARTICIPLE" in ana:
                self.tense = "PARTICIPLE"
            else:
                self.tense = None
                
        try:
            self.binyan = re.search(r'#BASEFORM_BINYAN_(\w+)', ana).group(1)
        except AttributeError:
            self.binyan = None


        phrases = root.iter('phrase')
        self.syntactic_attributes = None
        for phrase in phrases:
            if phrase.get('id') == self.phrase_id:
                self.syntactic_attributes = phrase.get('function')
                break

        xml_namespace = "{http://www.w3.org/XML/1998/namespace}"       
        pasuks = root.iter('s')
        for pasuk in pasuks:
            phrases = pasuk.iter('phrase')
            for p in phrases:
                if p.get('id') == self.phrase_id:
                    self.sentence = pasuk.get(f'{xml_namespace}id')
                    break
        
    @staticmethod
    def get_verb_info_xml(word): 
        for m in word.findall('m'):
            m.get('ana')
            if '#BASEFORM_POS_VERB' in m.get('ana') or "#BASEFORM_POS_PARTICIPLE" in m.get('ana'):
                return m
        return None
    
    @staticmethod
    def isverb_conllu(word):
        return word['upos'] == 'VERB'
    
    def DataFrame(self):
        data = {
        'text': self.text,
        'source': self.source,
        'sentence id': self.sentence,
        'lemma': self.lemma,
        'binyan': self.binyan,
        'number': self.number,
        'gender': self.gender,
        'person': self.person,
        'tense': self.tense,
        'phrase id': self.phrase_id,
        'syntactic attributes': self.syntactic_attributes
        }
        return pd.DataFrame(data, index=[0])
    
    def __str__(self):
        return f"{self.text[::-1]}:\t\tbinyan: {self.binyan}\tnumber: {self.number}\tperson: {self.person}\t tense: {self.tense}\t syntactic attributes: {self.syntactic_attributes}"