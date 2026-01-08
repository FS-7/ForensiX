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
            doc.append({ "encodings": fr.face_encodings(img, [loc])[0].tolist(), "location": loc, "file": image, "evidence": evidence, "case_id": case_id, "name": "", "group": "", "tags": [] })
        
        client.insert_many(doc)
        return True
    
    except Exception as e:
        return False

@app.route('/similarity', methods=["POST"])
def similarity():
    if len(request.form) < 1:
        return make_response("No data received", 400)
    
    data = request.form
    image = data["image"]
    enc_known = client.find({}, {"_id": 0}).to_list()
    #enc_unknown = []
    
    try:
        img = fr.load_image_file(image)
        for loc in fr.face_locations(img):
            for encoding in fr.face_encodings(img, [loc]):
                for enc in enc_known:
                    out = fr.compare_faces([enc["encodings"]], encoding, tolerance=0.5)
                    if out == np.True_:                    
                        outline = (255, 0, 0)
                        pil_img = Image.open(image)
                        pil_draw = ImageDraw.Draw(pil_img)
                        pil_img_db = Image.open(enc["file"])
                        pil_draw_db = ImageDraw.Draw(pil_img_db)
                        pil_draw.rectangle((loc[3], loc[0], loc[1], loc[2]), outline=outline)
                        pil_draw_db.rectangle((enc["location"][3], enc["location"][0], enc["location"][1], enc["location"][2]), outline=outline)
                        pil_img.show()
                        pil_img_db.show()
                        pil_img = None
                        pil_draw = None
                        pil_img_db = None
                        pil_draw_db = None
                        time.sleep(10)
                    
        return make_response("res", 200)
    except Exception as e:
        print(e)
    return make_response("Error", 200)
