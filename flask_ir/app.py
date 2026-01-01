from flask import Flask, request, session, make_response
from flask_cors import  CORS
from forensix.shared import *

import face_recognition as fr
import numpy as np

from pymongo import MongoClient
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

client = MongoClient(host="localhost", port=27017)["Forensix"]["Face_data"]

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(f"Face recognition model ready?: {str(fr.isLoaded() != None)}", 200)

@app.route("/", methods=["POST"])
def Image_AI():
    if len(request.form) < 1:
        return make_response("No files received", 400)
    try:    
        data = request.form
        image = data["image"]
        evidence = data["evidence"]
        case_id = data["case_id"]
        
        face_recognition(image, evidence, case_id)
        
        image_AI = ImageAI()
        raw_image = Image.open(image).convert('RGB')
        return make_response(image_AI.run(raw_image), 200)

    except Exception as e:
        return make_response("Error", 400)
    
def face_recognition(image, evidence, case_id):
    try:    
        doc = []
        img = fr.load_image_file(image)
        for loc in fr.face_locations(img):
            doc.append({ "encodings": fr.face_encodings(img, [loc])[0].tolist(), "location": loc, "file": image, "evidence": evidence, "case_id": case_id })
        
        client.insert_many(doc)
        return make_response("Success", 200)
    
    except Exception as e:
        return make_response("Error", 400)
    
@app.route('/similarity', methods=["POST"])
def similarity():
    if len(request.json) < 1:
        return make_response("No data received", 400)
    
    data = request.json
    enc_unknown = np.array(data["enc_unknown"])
    enc_known = np.array(data["enc_known"])
    
    try:
        res = str(fr.compare_faces([enc_known], enc_unknown, tolerance=0.3))
        return make_response(res, 200)
    except Exception as e:
        print(e)
    return make_response(str(e), 200)

@app.route('/similarity_list', methods=["POST"])
def similarity_list():
    if len(request.json) < 1:
        return make_response("No data received", 400)
    
    data = request.json
    
    enc_known = []
    for i in data["enc_known"]:
        enc_known.append(np.array(i))
    enc_unknown = np.array(data["enc_unknown"])
    
    try:
        res = str(fr.compare_faces(enc_known, enc_unknown, tolerance=0.3))
        return make_response(res, 200)
    except Exception as e:
        print(e)
        
    return make_response("", 200)
