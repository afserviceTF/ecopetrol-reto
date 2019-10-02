#------------------Importing Libraries------------------------#
import pandas as pd
import json
import os
from azureml.core.model import Model
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
#--------------------Defining the Init Function for the API----------------------#
def init():
    global model
    # retreive the path to the model file using the model name
    model_path = Model.get_model_path('ecopetrol')
    #model = load_model(model_path)
    model = joblib.load(model_path)
   

#-------------------Defining the Run Function for the API------------------------#
def run(raw_data):
    #cargando los datos
    #data = np.array(json.loads(raw_data)['data'])
    df_pred = pd.DataFrame()    
    df_pred = df_pred.from_dict(json.loads(raw_data), orient='index')

    #dataframe con las variables
    dfX_pred = df_pred[['Diameter', 'Height', 'Length', 'Shell weight', 'Shucked weight',
       'Viscera weight', 'Whole weight']]
    #Transformar las X's con la función MinMaxScaler()
    scaler = StandardScaler()
    dfX_pred_tr = scaler.fit_transform(dfX_pred)

    # Generar predicción
    prediction=model.predict(dfX_pred_tr)

    #agregando prediccion al df
    df_pred['PREDICCION'] = prediction

    # you can return any data type as long as it is JSON-serializable
    return df_pred[['PREDICCION']].values.tolist()
