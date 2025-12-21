from flask import Flask, request, make_response, session
from flask_cors import CORS

from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import tempfile
import torch
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

device = "cpu"
dtype = torch.float32
batch_size = 12
language = 'en'
timestamps = True

asr = None

class ASR:
    def __init__(self, device, compute_type):
        self.model = None
        self.__asr = "openai/whisper-large-v3"
        self.__load_model(device, compute_type)
    
    def __load_model(self, device, compute_type):
        
        self.model = pipeline("automatic-speech-recognition", model=self.__asr, device=device, dtype=str(compute_type).split(".")[1])
        
        if self.model != None:
            print(f"{self.__asr} Loaded!")
            
    def isLoaded(self):
        return False if self.model == None else True

asr = ASR(device, dtype)

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(f"ASR Model Ready?:{str(asr.isLoaded() != None)}", 200)
   
@app.route('/', methods=["POST"])
def ask_whisperx():
    data = request.files
    audio_file = data["audio"]
    
    print(audio_file)
    
    output = {}
    
    temp_file_name = ""
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as temp_file:
        audio_file.save(temp_file)
        temp_file_name = temp_file.name
        output = asr.model(temp_file_name, return_timestamps=timestamps, language=language)

    return make_response(output, 200)
