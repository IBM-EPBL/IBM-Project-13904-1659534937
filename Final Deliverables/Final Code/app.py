from flask import Flask , request , redirect
import os
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics

from flask import render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "LUNFExi5WKFc6FnwVbnbTCOW0-8UdaydjLkuTvrcaa_T"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app=Flask(__name__)

@app.route("/")
def index():
    print(os.getcwd())
    return render_template("Start-Page.html",score=100)

@app.route("/predict",methods=['POST'])
def predict():
    gre_score=request.form["gre"]
    toefl_score=request.form["toefl"]
    ur_value=request.form["ur"]
    lor_score=request.form["lor"]
    sop_score=request.form["sop"]
    cgpa_value=request.form["cgpa"]
    rp_value=request.form["rp"]
    t=[[int(gre_score),int(toefl_score),int(ur_value),int(lor_score),int(sop_score),int(cgpa_value),int(rp_value)]]
    payload_scoring = {"input_data": [{"fields": [['GRE Score','TOEFL Score','University Rating','SOP','LOR','CGPA','Research']], "values": t }]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5759ccd2-2dd9-4897-beae-1ed5286a8fb3/predictions?version=2022-11-16', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    output= response_scoring.json()["predictions"][0]["values"][0][0]
    op=(output*100)
    while op>=100:
        op-=2
    while op<5:
        op+=5
    op=round(op,2)
    if op>=50:
        return render_template("success.html",score=op)
    else:
        return render_template("fail.html",score=op)

if __name__ == "__main__":
    app.run(debug=True)