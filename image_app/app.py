# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 08:09:55 2019

@author: Diana Acosta
"""

#!flask/bin/python
import requests
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import render_template, redirect, url_for
#import pandas as pd
import cv2 as cv
import numpy as np
import pandas as pd
import json

app = Flask(__name__)




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/ecopetrol/api/v1.0/', methods=['GET'])
def get_hello():
    return  "<img src='static/fruit.jpg'/>"

@app.route('/gallery')
def get_gallery():
    #return "<img src='static/s.jpg'/>"  
    if request.args:
        print('acaa')
        return render_template("resultado.html", message=json.dumps({"message":"alerta"}))
    return render_template("resultado.html")


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/detection")
def detection():
    return render_template('cascos.html')


@app.route('/ecopetrol/api/v1.0/', methods=['POST'])
def detect_helment():
    if request.method == 'POST':
        endpoint = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/21be4d2c-fa3a-4c44-ba22-2360b047742c/detect/iterations/cascos/image'
        image = request.files['file'].read()
        nparr = np.fromstring(image, np.uint8)
        img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)
        #image.save('C:/Users/Diana Acosta/OneDrive - Idata/Ecopetrol/Reto/asd.jpg')              
        headers = {
            'Prediction-Key': '177f19ca3b8448a5a3f8909315098d41',
            'Content-Type': 'application/octet-stream'
        }
        resp = requests.post(endpoint, data=image, headers=headers)
        resp = resp.json()        
        # imgHeight, imgWidth, channels = img_np.shape      
        imgWidth = img_np.shape[1] 
        imgHeight = img_np.shape[0]    
        aux = 0
        for prediction in resp['predictions']:
        
            probabilidad = float(prediction['probability'])*100
            if probabilidad > 60:
                aux = 1
                #print ("\t" + prediction['tagName'] + ": {0:.2f}%".format(prediction['probability'] * 100), prediction['boundingBox']['left'], prediction['boundingBox']['top'], prediction['boundingBox']['width'], prediction['boundingBox']['height'])
                left = int(prediction['boundingBox']['left']* imgWidth)
                top = int(prediction['boundingBox']['top']*imgHeight)
                width = int(left + (prediction['boundingBox']['width']*imgWidth))
                height = int(top + (prediction['boundingBox']['height']*imgHeight))
                frame = cv.rectangle(img_np, (left, top), (width,height), (0,255,255), 2)
                
                cv.imwrite('static/s.jpg',frame)
        
        if aux == 0:
             cv.imwrite('static/s.jpg',img_np)
             mesg = json.dumps({"mensaje":"alerta"})
             return redirect(url_for('get_gallery', message=mesg))
     
        #response = make_response(jsonify(resp, 200))
        return redirect(url_for('get_gallery'   ))
    else:
        response = make_response(
                jsonify({'error': 'Imagen no encontrada'}), 
                404)
    
        return response
    
@app.route('/fishes', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    results = []
    if request.method == 'POST':  #this block is only entered when the form is submitted
        Diameter = request.form.get('Diameter')
        Height = request.form.get('Height')
        Length = request.form.get('Length')
        Shellweight = request.form.get('Shellweight')
        Shuckedweight = request.form.get('Shuckedweight')
        Visceraweight = request.form.get('Visceraweight')
        Wholeweight = request.form.get('Wholeweight')
       
        data=pd.DataFrame([{'Diameter':Diameter,'Height':Height, 'Length':Length, 'Shell weight':Shellweight, 'Shucked weight':Shuckedweight, 'Viscera weight':Visceraweight, 'Whole weight': Wholeweight}])
        #data=pd.DataFrame([{'Diameter':0.7,'Height':0.185, 'Length':18.075, 'Shell weight':0.38, 'Shucked weight':0.48, 'Viscera weight':0.67, 'Whole weight': 0.78, 'Sex_1.0':1}])

        try:
                print('importando paquetes necesarios')
                           
                print('Preparando la info para la llamada a la api')
                url = 'http://13.92.187.54:80/api/v1/service/deplyecopetrol/score'
                headers = {'Content-Type':'application/json', 'Authorization':'Bearer mHocfOihNwgQkKYDnE5t0H2tNEm7hv92'}
                #data = pd.read_csv("C:/Users/Usuario/Documents/ecopetrol/reto/pescados_prueba.csv", sep = ';')
                data = data.to_dict(orient = 'index')
                data = json.dumps(data)
                #data=data[0]
               
            
                print('Llamando la api')
                response = requests.post(url, headers = headers, data = data)
                print(response.text)
                print('Estructurando los resultados')
                results = json.loads(response.text)
                print(results)
                #results = pd.DataFrame(results)
                #print(results)
                #results.columns = ['RESULTS']
                print("\n")
               # print(results)
                print("\n")
                print('Escribiendo en un CSV')
                #results.to_csv("C:\\Users\\Usuario\\Documents\\ecopetrol\\reto\\pescadores\\results.csv", sep = ';', index = False)
                print('PROCESO TERMINADO')
            
        except:
                print('ERROR')
         
        return render_template('fishes_result.html', value=np.round(results[0][0]))
    
    """"""
    return render_template('fishes.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

        

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    
#
