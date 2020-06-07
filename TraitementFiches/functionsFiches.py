# -*- coding: utf-8 -*-
import functions as fun
import pandas as pd
import nltk
from Classes import Fonction, Image, Source, EltArchi

def read_data(filename):
    data= pd.read_csv(filename, encoding='utf-8')
    return data


aspectSoc= "Social"
aspectEnv ="Environnemental"
aspectArchi="Architectural"
def get_files_data(file):
    df_elts= fun.read_data(file)
    elts=[]
    for i in range(0, df_elts.shape[0]):
        id =i
        j= i*3
        nom =  df_elts['Elément'][i]
        appelTradi= df_elts['Appellation traditionnelle'][i]
        desc = df_elts['Définition'][i]

        image = df_elts['Illustration'][i]
        images = []
        if image != "Pas d'image":
            imgs = nltk.tokenize.sent_tokenize(image)
            for y in range(0, len(imgs)):
                img = Image.Image(j + y, imgs[x], "")
                images.append(img)

        foncts=[]
        nomFonctSoc=df_elts['Fonction'][i]
        fonc1 = Fonction.Fonction(j,nomFonctSoc,aspectSoc)
        foncts.append(fonc1)

        nomFonctArchi = df_elts['Relation'][i]
        fonc2 =Fonction.Fonction(j+1, nomFonctArchi, aspectArchi)
        foncts.append(fonc2)

        nomFonctEnv = df_elts['Dispositif environnemental'][i]
        fonc3 = Fonction.Fonction(j+2, nomFonctEnv, aspectEnv)
        foncts.append(fonc3)
        categorie= df_elts['Catégorie'][i]


        sources=[]
        srcs= df_elts['Documentation/source'][i]
        sents= nltk.tokenize.sent_tokenize(srcs)
        for x in range(0,len(sents)):
            src= Source.Source(j+x, sents[x], "")
            sources.append(src)
        elt=EltArchi.EltArchi(i, nom, appelTradi, desc, categorie, foncts,sources, images)


    elts.append(elt)

    return elts
