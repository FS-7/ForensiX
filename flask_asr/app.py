from flask import Flask, request, make_response, session
from flask_cors import CORS

from faster_whisper import WhisperModel, BatchedInferencePipeline
import torch
import warnings

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

device = "cuda"
batch_size = 16
language = 'en'

torch.cuda.empty_cache()

asr = None

class ASR:
    def __init__(self, device, compute_type):
        self.model = None
        self.__asr = "large-v3"
        self.__load_model(device, compute_type)
    
    def __load_model(self, device, compute_type):
        model = WhisperModel("large-v3", device=device, compute_type=compute_type)
        self.model = BatchedInferencePipeline(model=model)
        
        if self.model != None:
            print(f"{self.__asr} Loaded!")
            
    def isLoaded(self):
        return False if self.model == None else True

asr = ASR(device, "int8")

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(f"ASR Model Ready?:{str(asr.isLoaded() != None)}", 200)
   
@app.route('/', methods=["POST"])
def ask_whisperx():
    data = request.form
    audio_file = data["audio"]
    
    print(audio_file)
    
    output = []
    segments, _ = asr.model.transcribe(audio_file, language='en', batch_size=batch_size)
    for segment in segments:
        output.append(segment.text)
        
    return make_response(" ".join(output), 200)
