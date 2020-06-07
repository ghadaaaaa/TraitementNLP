import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
import re
import nltk
#nltk.download('punkt')
import pandas as pd
from pandas import DataFrame
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
nlp= spacy.load('fr_core_news_md')


sud = {'Ghardaia', 'Ouargla', 'Timimoun'}
maisons = {'maison', 'dar', 'ksar', 'kasr', 'palais'}

def read_data(filename):
    data= pd.read_csv(filename, encoding='utf-8')
    return data


def check_maison(df_elts, i):
    if (df_elts['Region'][i] not in sud):

        doc = nlp(df_elts['Element'][i])
        for tok in doc:
            if tok.text.lower() in maisons:
                return True
            else:
                return False


def extract_adresse(sent):
    sent = sent.replace('-', ' ')
    doc = nlp(sent)
    adresseMatcher = Matcher(nlp.vocab)
    patternAdresse = [{'lower': 'quartier'}, {'is_alpha': True, 'op': '+'}]
    adresseMatcher.add("Adresse", None, patternAdresse)
    matches = adresseMatcher(doc)
    results = [doc[start:end] for match_id, start, end in matches]
    return (results[-1])


def extact_info_construction(sent):
    # Extraire l'année de construction:
    annee = re.findall(r'(\d{4})', sent)
    doc = nlp(sent)
    # Extraire toutes les entitées de type personne (Constructeurs + Fondateurs):
    pers = [ent.text for ent in doc.ents if ent.label_ == 'PER']

    # Extraire le/les fondateurs:
    fondateurmatcher = PhraseMatcher(nlp.vocab)
    patternFondateur = [nlp.make_doc(name) for name in ["Yahia Rais", "Dey Hassan"]]
    fondateurmatcher.add("Fondateurs", None, *patternFondateur)
    fondateurs = []
    for match_id, start, end in fondateurmatcher(doc):
        fondateurs.append(str(doc[start:end]))

    # liste des constructeurs:
    constructeurs = [per for per in pers if per not in fondateurs]

    return (annee, fondateurs, constructeurs)


def extract_classement(sent):
    doc = nlp(sent)
    # Extraire l'année de construction:
    annees = re.findall(r'(\d{4})', sent)
    annee = str(annees[0])
    entis = [str(ent.text) for ent in doc.ents if ent.label_ == 'ORG']
    org = []
    if entis:
        org = entis
    else:
        num = int(annee, 10)
        if num <= 1962:
            org = "L'état français"
        else:
            org = "L'état algérien"

    return (annee, org)


def extract_prop(sent):
    doc= nlp(sent)
    entis = [ent.text for ent in doc.ents ]
    proprietaires=[]
    for x in entis:
        if x not in proprietaires:
            proprietaires.append(x)
    return proprietaires

def extract_rehabi(sent):
  doc= nlp(sent)
  annees= re.findall(r'(\d{4})', sent)
  annees=[str(annee) for annee in annees]
  return annees