from flask import Flask, request, session, make_response
from flask_cors import  CORS

import face_recognition as fr
import numpy as np
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(f"Face recognition model ready?: {str(fr.isLoaded() != None)}", 200)

@app.route("/", methods=["POST"])
def face_recognition():
    if len(request.files) < 1:
        return make_response("No files received", 400)
    
    data = request.files
    image = data["image"]
    
    locations = fr.face_locations(fr.load_image_file(image))
    doc = []
    for i, l in enumerate(locations):
        enc = fr.face_encodings(fr.load_image_file(image), [l])[0]
        doc.append((i, enc.tolist(), l, image.name))
        print(len(enc))
    
    return make_response(doc, 200)

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
