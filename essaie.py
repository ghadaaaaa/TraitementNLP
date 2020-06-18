import spacy
nlp = spacy.load('fr_core_news_md')
doc1 = nlp("construire")
doc2 = nlp("construire")
print(doc1.similarity(doc2))