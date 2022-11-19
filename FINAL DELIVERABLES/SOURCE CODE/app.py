# import the necessary packages

import numpy as np
import requests
import pandas as pd
import pickle
import os


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "yqT_PSaI78UdDvF5NHCsAcCuoum8egG14-TM5-nwLstc"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                     API_KEY,"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


from flask import Flask, request, render_template

app = Flask(__name__, template_folder="Templates")


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')


@app.route('/pred', methods=['GET'])
def page():
    return render_template('upload.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict(input_features=None):
    print("[INFO] loading model...")
    #model = pickle.load(open('fdemand.pkl', 'rb'))
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    print(features_value)

    payload_scoring = {"input_data": [{"field": [["homepage_featured", "emailer_for_promotion", "op_area", "cuisine",
                                                  "city_code", "region_code", "category"]],
                                       "values": [input_features]}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/11ac2294-65d5-4aec-af1f-eda82b69d29d/predictions?version=2022'
        '-11-11', json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions = response_scoring.json()
    print(predictions)
    print("Final Prediction Result", predictions['predictions'][0]['values'][0][0])
    pred = predictions['predictions'][0]['values'][0][0]

    #features_name = ['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine','city_code', 'region_code', 'category']
    #prediction = model.predict(features_value)
    #output = prediction[0]
    print(pred)
    return render_template('upload.html', prediction_text=pred)


if __name__ == '__main__':
    app.run(debug=False)
