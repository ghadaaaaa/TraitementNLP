# -*- coding: utf-8 -*-
from TraitementFiches import functionsFiches as fun
import json
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello World!</h1>"


@app.route('/alawi/', methods = ['POST'])
def alawi():
    if request.method == 'POST':
        decoded_data = request.data.decode('utf-8')
        params = json.loads(decoded_data)
        if (params['typeMaison']== "alawi"):
            file = "FichesCSV\Alawi\EltsMaisonAlawi.csv"
            elts = fun.get_files_data(file)
            results=[]

            for elt in elts:
                fonctions=[]
                fonctions.clear()
                for fonction in elt.fonctions:
                    fonctions.append({'idFonction': fonction.idFonction, 'fonction': fonction.descFonction,
                                      'aspectFonction': fonction.aspectFonction})

                images=[]
                for image in elt.images:
                    images.append({'idImage': image.idImage, 'image': image.pathImage, 'legende': image.legende})

                sources =[]
                for source in elt.sources:
                    sources.append({'idSource': source.idSource, 'source': source.source, 'typeSource': source.typeSource})

                results.append({'idEltArchi': elt.idEltArchi,
                                'nomEltArchi': elt.nomEltArchi,
                                'appelTradi' : elt.appelTradi,
                                'descEltArchi': elt.descEltArchi,
                                'typeEltArchi': elt.typeEltArchi,
                                'fonctions': fonctions,
                                'images': images,
                                'sources': sources})
    return jsonify({'results': results})



if __name__=='__main__':
    app.run(debug=True)












