import spacy
from spacy.matcher import Matcher
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
import csv
import functions as fun
import Maison as m
nlp= spacy.load('fr_core_news_md')

Results =[["Casbah d'Alger", 'Alger', "Dans l’un des plus beaux sites maritimes de la Méditerranée, surplombant les îlots où un comptoir carthaginois fut installé dès le IVe siècle av. J.-C., la Casbah constitue un type unique de médina , ou ville islamique. Lieu de mémoire autant que d’histoire, elle comprend des vestiges de la citadelle, des mosquées anciennes, des palais ottomans, ainsi qu’une structure urbaine traditionnelle associée à un grand sens de la communauté."],
         ["Dar khdaouedj el amia", "Alger", "Dar Khedaoudj El Amia se situe au niveau du quartier Souk-el-Djemâa bordant la rue Mohamed Malek. Authentique palais construit en 1570 par Yahia Rais officier de la flotte algérienne. Propriété de la fille du Dey, elle fut occupée par le trésorier du Dey Med Ben Athmane, elle fut ensuite, La 1ere Mairie Française d'Alger. En 1909, elle devient l'hôtel particulier du premier président de la cour d'appel. En 1947 elle est aménagée en maison d'artisanat. Classée en 1887, elle abrite actuellement le musée des arts et traditions populaires depuis 1987. Elle a subi des travaux de réhabilitation après 2003."],
         ["Timgad", "Batna","Sur le versant nord des Aurès, Timgad fut créée ex nihilo, en 100 apr. J.-C., par l'empereur Trajan comme colonie militaire. Avec son enceinte carrée et son plan orthogonal commandé par le cardo et le decumanus, les deux voies perpendiculaires qui traversaient la ville, c'est un exemple parfait d'urbanisme romain. Ce palais fût construit en 1791 par le Dey d’Alger Hassen El-Kheznadji dit Baba Hassen ; a connu des vicissitudes :Siège du 1er gouverneur Français.Hôtel des hautes personnalités en mission, Institut de la langue arabe. Siège des affaires religieuses. Il est constitué de 03 maisons : Dar Hassen Pacha ainsi que de 02 maisons mitoyennes de la rue Cheikh El Kinai.Classé en 1887 ce palais est en cours de travaux de restauration."],
         ["Dar hassan Bacha", "Alger", "Dar Hassen Pacha « le palais d’hiver » se situe dans la basse Casbah dans le quartier Souk-el-Djemâa en face Dar Aziza mitoyenne à la mosquée Ketchaoua bordant la place Cheikh Ben Badis."]
         ]


with open('eltsPatri.csv' ,'w', newline='') as f:
    fieldnames=['Element','Region','Texte', 'Maison','Espace','Monument','Site']
    thewriter= csv.DictWriter(f, fieldnames=fieldnames)
    thewriter.writerow({'Element':'Element','Region':'Region','Texte':'Texte','Maison':'Maison','Espace':'Espace','Monument':'Monument',
                      'Site':'Site'})
    for elt in Results:
        thewriter.writerow({'Element':elt[0],'Region': elt[1], 'Texte':elt[2]})

df_elts= pd.read_csv("eltsPatri.csv", encoding='cp1252')
print(df_elts)

for i in range(0, df_elts.shape[0]):
    df_elts['Maison'][i]= fun.check_maison(df_elts, i)
print(df_elts)

#df pour les maison
df_Maison=df_elts.loc[df_elts['Maison']==True].copy()
df_Maison.drop(['Maison'], axis = 1,inplace=True)
df_Maison.drop(['Espace'], axis = 1,inplace=True)
df_Maison.drop(['Monument'], axis = 1,inplace=True)
df_Maison.drop(['Site'], axis = 1,inplace=True)
df_Maison.to_csv('Maisons.csv', index=False, encoding='utf-8')
print(df_Maison)
df_mais= pd.read_csv("Maisons.csv", encoding='utf-8')
print(df_mais)


######################################


# Données du SITE DU CNRA:
patternRelation = [{'POS': 'VERB'}]
matcher = Matcher(nlp.vocab)
matcher.add("matching_Relation", None, patternRelation)
maisonsCNRA = []
for i in range(0, df_mais.shape[0]):
    id = i
    text = df_mais['Texte'][i]
    name = df_mais['Element'][i]
    adresse = ""
    dateCnstr = ""
    constructeurs = []
    fondateurs = []
    proprietaires = []
    dateClass = ""
    org = ""
    dateRehabi = []
    sents = sent_tokenize(text)
    for sent in sents:
        print(sent)
        doc = nlp(sent)
        matches = matcher(doc)

        verbs = [doc[start:end] for match_id, start, end in matches]
        print(verbs)
        i = 0
        continuAdresse = True
        continuConstr = True
        continuClass = True
        while continuAdresse == True and i < len(verbs) and continuConstr == True and continuClass == True:
            simAdr = verbs[i].similarity(nlp("situe"))
            simConstr = verbs[i].similarity(nlp("construit"))
            simClass = verbs[i].similarity(nlp("classée"))
            i = i + 1
            if (simAdr >= 0.8):
                continuAdresse = False
            if (simConstr >= 0.8):
                continuConstr = False
            if (simClass >= 0.8):
                continuClass = False
        # Adresse:
        if continuAdresse == False:
            adresse = fun.extract_adresse(sent)
            print(adresse)
        # Info sur la construction:
        if continuConstr == False:
            dateCnstr, constructeurs, fondateurs = fun.extact_info_construction(sent)
            print(dateCnstr)
            print(constructeurs)
            print(fondateurs)
        if continuClass == False:
            dateClass, org = fun.extract_classement(sent)
            print(dateClass)
            print(org)

        # info sur les propriétaires:
        tokens = []
        for tok in doc:
            tokens.append(tok.text)
        continuProp = True
        continuRehabi = True
        i = 0
        while i < len(tokens) and continuProp == True:
            simProp = max(nlp(tokens[i]).similarity(nlp("propriété")), nlp("propriétaire").similarity(nlp(tokens[i])))
            simRehabi = max(nlp(tokens[i]).similarity(nlp("réhabilitation")),
                            nlp("restaurer").similarity(nlp(tokens[i])))
            i = i + 1
            if simProp > 0.8:
                continuProp = False
            if simRehabi > 0.8:
                continuRehabi = False
        if continuRehabi == False:
            dateRehabi = fun.extract_rehabi(sent)
            print(dateRehabi)
        if continuProp == False:
            proprietaires = fun.extract_prop(sent)
            print(proprietaires)
        print("***SENTENCE***")
    maison = m.Maison(id, name, text, adresse, dateCnstr, constructeurs, fondateurs, proprietaires, dateClass, org, dateRehabi)
    maisonsCNRA.append(maison)
    print("*******************************************************END******")

######################################

for mai in maisonsCNRA:
  print(mai.id)
  print(mai.name)
  print(mai.adresse)
  print(mai.org)



#LE SITE DES CARTES PATRIMOINE CULTUREL ALGERIEN:

ResultsCartes =[["Dar khdaouedj el amia", "Alger", "Le Musée National des Arts et Traditions Populaires se trouve dans le quartier de la basse casbah nommé Socgemah (souk el djemaa). Il est appelé Souk el djemaa en rapport au marché qui s’y déroulait chaque vendredi pour commercialiser les volatiles de tous genres : oiseaux, pigeons, poules ..."]
               ]