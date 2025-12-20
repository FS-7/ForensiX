from flask import Flask, request, make_response, session
from flask_cors import CORS

import whisperx
import tempfile
import torch
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

device = "cpu" #if torch.cuda.is_available() else "cpu"
dtype = torch.float32
batch_size = 12
language = "en"
asr = None

class ASR:
    def __init__(self, device, compute_type):
        self.model = None
        self.__asr = "large-v3"
        self.__load_model(device, compute_type)
    
    def __load_model(self, device, compute_type):
        self.model = whisperx.load_model(self.__asr, device, compute_type=str(compute_type).split(".")[1])
        if self.model != None:
            print(f"{self.__asr} Loaded!")
            
    def isLoaded(self):
        return False if self.model == None else True

asr = ASR(device, dtype)

@app.route('/')
def main():
    return make_response("", 200)

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(f"ASR Model Ready?:{str(asr.isLoaded() != None)}", 200)
   
@app.route('/asr', methods=["POST"])
def ask_whisperx():
    data = request.files
    audio_file = data["audio"]
    try:
        output = {}
        with tempfile.NamedTemporaryFile(mode="wb", delete=True) as temp_file:
            audio_file.save(temp_file)
            temp_file_name = temp_file.name
            audio = whisperx.load_audio(temp_file_name)
            output = asr.model.transcribe(audio, batch_size=batch_size)

        return make_response(output, 200)
    
    except Exception as e:
        print(e)
    return make_response("", 500)
