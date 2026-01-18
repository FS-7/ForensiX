from flask import Flask, request, session, make_response
from flask_cors import  CORS
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image, ImageDraw
from pymongo import MongoClient

import face_recognition as fr
import numpy as np
import warnings
import time

warnings.filterwarnings("ignore")

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

client = MongoClient(host="localhost", port=27017)["Forensix"]["Face_data"]
val = MongoClient(host="localhost", port=27017)["Forensix"]["i"]
image_AI = None

class ImageAI:
    def __init__(self, img_ai = "Salesforce/blip-image-captioning-large"):
        self.__img_ai = img_ai
        self.__processor = None
        self.__model = None
        self.__load_model()
    
    def __load_model(self):        
        self.__processor = BlipProcessor.from_pretrained(self.__img_ai)
        self.__model = BlipForConditionalGeneration.from_pretrained(self.__img_ai).to("cuda")
    
    def run(self, raw_image):
        inputs = self.__processor(raw_image, return_tensors="pt").to("cuda")
        out = self.__model.generate(**inputs)
        return self.__processor.decode(out[0], skip_special_tokens=True)

    def isLoaded(self):
        return False if self.__model == None else True
    
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
        
        #face_recognition(image, evidence, case_id)
        
        image_AI = ImageAI()
        raw_image = Image.open(image).convert('RGB')
        output = image_AI.run(raw_image)
        return make_response(output, 200)

    except Exception as e:
        return make_response("Error", 400)
    
def face_recognition(image, evidence, case_id):
    i = val.find({}, {"_id": 0})[0]["i"]
    try:    
        doc = []
        enc_known = client.find({}, {"_id": 0}).to_list()
        
        img = fr.load_image_file(image)
        for loc in fr.face_locations(img):
            for encoding in fr.face_encodings(img, [loc]):
                    
                res = None
                for enc in enc_known:
                    out = fr.compare_faces([enc["encodings"]], encoding, tolerance=0.57)
                    print(out)
                    if out == np.True_:
                        print(enc["group"])
                        res = enc["group"]
                        
                if res == None:
                    doc.append({ "encodings": encoding.tolist(), "location": loc, "file": image, "evidence": evidence, "case_id": case_id, "name": "", "group": f"group_{i}", "tags": [] })
                    i = i + 1
                else:
                    doc.append({ "encodings": encoding.tolist(), "location": loc, "file": image, "evidence": evidence, "case_id": case_id, "name": "", "group": res, "tags": [] })
                                 
        print(doc)
        val.update_one({}, {'$set': {"i": i}})
        client.insert_many(doc)
        return True
    
    except Exception as e:
        return False
