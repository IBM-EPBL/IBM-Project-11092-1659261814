import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "yqT_PSaI78UdDvF5NHCsAcCuoum8egG14-TM5-nwLstc"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                     API_KEY,"grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"field": [["homepage_featured", "emailer_for_promotion", "op_area", "cuisine",
                                               "city_code", "region_code", "category"]], "values": [[0, 0, 2.0, 3, 647,
                                                                                                     56, 0]]}]}

response_scoring = requests.post(
    'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/11ac2294-65d5-4aec-af1f-eda82b69d29d/predictions?version=2022'
    '-11-11', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
predictions = response_scoring.json()
print(predictions)
print("Final Prediction Result", predictions['predictions'][0]['values'][0][0])
pred=predictions['predictions'][0]['values'][0][0]