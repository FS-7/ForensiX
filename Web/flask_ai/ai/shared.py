from flask import Flask, request, make_response, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from transformers import pipeline, logging

import whisperx
import torch 
import json
import tempfile
import os
import warnings

warnings.filterwarnings("ignore")
logging.set_verbosity_error()

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
batch_size = 12
language = "en"

ALLOWED_EXTENSIONS = {'.mp3', '.mpeg', '.obb', '.m4a'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
class ASR:
    def __init__(self, device, compute_type):
        self.model = None
        self.__asr = "large-v3"
        self.load_model(device, compute_type)
    
    def load_model(self, device, compute_type):
        self.model = whisperx.load_model(self.__asr, device, compute_type=str(compute_type).split(".")[1])
        if self.model != None:
            print(f"{self.__asr} Loaded!")
            
    def isLoaded(self):
        return False if self.model == None else True
    
class NLP:
    def __init__(self, device, compute_type):
        self.__nlp = "google/gemma-2-2b-it"
        self.model = None
        self.load_model(device, compute_type)
    
    def load_model(self, device, compute_type):
        self.model = pipeline("text-generation", model=self.__nlp, model_kwargs={"torch_dtype": compute_type}, device=device)
        if self.model != None:
            print(f"{self.__nlp} Loaded!")
        
    def isLoaded(self):
        return False if self.model == None else True

asr = ASR(device, torch_dtype)
nlp = NLP(device, torch_dtype)
     