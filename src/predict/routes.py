from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from sklearn.preprocessing import StandardScaler
from joblib import load
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import numpy as np
import pandas as pd 
import os

predict_router = APIRouter()

scaler = StandardScaler()

class FileDetails(BaseModel):
    filename: str
    model: str

class ModelFile(BaseModel):
    files: list[str]
    models: list[str]

@predict_router.post('/upload', status_code=201)
async def upload_test_file(uploaded_file: UploadFile):
    # return { "filename": file.filename }
    filepath = os.getcwd()
    filepath = filepath.replace('\\', '/')
    file_location = f"{filepath}/src/files/{uploaded_file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded_file.file.read())

    return {"info": f"file '{uploaded_file.filename}' saved at '{file_location}'"}

@predict_router.post('/file-predict')
async def predict_file(filedetails: FileDetails):

    filename = filedetails.filename
    modelname = filedetails.model

    filepath = os.getcwd()
    filepath = filepath.replace('\\', '/')
    modelpath = ''
    modelpath = filepath
    filepath = filepath + '/src/files/' + filename

    if modelname == 'K-Means':
        modelpath = modelpath + '/src/trained models/' + 'kmeans_model.pkl'

    else:
        modelpath = modelpath + '/src/trained models/' + 'spectral_model.pkl'

    print(filepath)
    print(modelpath)

    kmeans_loaded = load(modelpath)
    new_data = pd.read_csv(filepath)

    new_data.rename(columns={
        'Urban/Rural': 'Place',
        'Purchase History': 'Purchased Product',
        'Average Order Value (AOV)': 'Average Order Value',
        'Customer Satisfaction (CSAT)': 'Customer Satisfaction'
    }, inplace=True)

    new_data.dropna(inplace=True)
    new_data = pd.get_dummies(new_data, columns=['Gender', 'Income Level', 'Region', 'Purchased Product', 'Place', 'Festival Engagement'], drop_first=True)

    features = new_data[['Age', 'Average Order Value', 'Customer Satisfaction'] + 
                list(new_data.columns[new_data.columns.str.startswith(('Gender_', 'Income Level_', 'Region_', 'Purchased Product_', 'Place_', 'Festival Engagement_'))])]

    # Normalize the features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    predictions = kmeans_loaded.predict(features_scaled)
    print(predictions)
    # json_compatible_item_data = jsonable_encoder(predictions)
    # return JSONResponse(content=json_compatible_item_data)

    return { "message": f"Predicted Successfully. Number of Clusters formed in this dataset is { len(np.unique(predictions)) }"}

@predict_router.get('/details')
async def get_model_files():
    filepath = os.getcwd()
    filepath = filepath.replace('\\', '/')

    filepath = filepath + '/src/files/'
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    print(onlyfiles)

    models = ['K-Means', 'Spectral-Clustering']

    json_compatible_item_data = jsonable_encoder(ModelFile(files=onlyfiles, models=models))
    return JSONResponse(content=json_compatible_item_data)