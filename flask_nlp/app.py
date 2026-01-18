from flask import Flask, request, make_response, session
from flask_cors import CORS
from transformers import pipeline, logging

import torch
import json
import os

app = Flask(__name__)
cors = CORS(app)

torch.cuda.empty_cache()

device = "cuda:0" if torch.cuda.is_available() else "cpu"
dtype = torch.float32
batch_size = 12
nlp = None

class NLP:
    def __init__(self, device, compute_type):
        self.__nlp = "google/gemma-2-2b-it"
        self.model = None
        self.__load_model(device, compute_type)
    
    def __load_model(self, device, compute_type):
        self.model = pipeline("text-generation", model=self.__nlp, model_kwargs={"dtype": compute_type}, device=device)
        if self.model != None:
            print(f"{self.__nlp} Loaded!")
        
    def isLoaded(self):
        return False if self.model == None else True

nlp = NLP(device, dtype)
     
@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(f"NLP Model Ready?: {str(nlp.isLoaded() != None)}", 200)
   
@app.route('/', methods=["POST"])
def ask_gemma():
    try:
        data = json.loads(request.data)
        messages = data["messages"]
        new_token_size = int(data["new_token_size"])
        
        outputs = nlp.model(messages, max_new_tokens=new_token_size)
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
        return make_response(assistant_response, 200)
        
    except Exception as e:
        print(e)
        return make_response("", 400)