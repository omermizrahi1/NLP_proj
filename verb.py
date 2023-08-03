
import os
import time
from conllu import parse
from conllu.models import Token as Token
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element as Element
import re
import pandas as pd
from enum import Enum




class Verb:
    def __init__(self, init_type: str, word, src_file: str, sentences = None):
        if init_type == "conllu":
            self.conllu_init(word, src_file, sentences)
        else:
            raise ValueError("Invalid init_type")
        
    ###  CONLLU  ###
    def conllu_init(self, word: Token, src_file: str, sentences):
        if sentences is None:
            raise ValueError("sentences is None")
        #if not self.isword_conllu(word):
         #   raise ValueError("Word is not a verb")
        self.phrase_id = word['id']
        self.lemma = word['lemma']
        self.text = word['form']
        self.pos = word['xpos']
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
            
        
    @staticmethod
    def isverb_conllu(word):
        return word['upos'] == 'VERB'
    
    @staticmethod
    def isword_conllu(word):
        if len(word['form']) == 1:
            return word['form'] in '0123456789'  # Hebrew alphabet
        if isinstance(word['id'], int):
            return True
        else:
            return not any('-' in str(item) for item in word['id'])
    
    def DataFrame(self):
        data = {
        'POS': self.pos,
        'GENDER': self.gender,
        'NUMBER': self.number,
        'text': self.text,
        'lemma': self.lemma,
        'sentence id': self.sentence,
        'person': self.person,
        'index': self.phrase_id,
        'syntactic attributes': self.syntactic_attributes,
        'tense': self.tense,
        'binyan': self.binyan
        }
        return pd.DataFrame(data, index=[0])
    
    def __str__(self):
        return f"{self.text[::-1]}:\t\tbinyan: {self.binyan}\tnumber: {self.number}\tperson: {self.person}\t tense: {self.tense}\t syntactic attributes: {self.syntactic_attributes}"