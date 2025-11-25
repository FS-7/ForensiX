from ai.shared import *

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(str(asr != None and nlp != None), 200)
    
@app.route('/asr')
def ask_whisperx():
    data = request.data
    audio_path = data["audio"]
    audio = asr.model.load_audio(audio_path)
    return asr.model.transcribe(audio, batch_size=batch_size, language='en')

@app.route('/nlp')
def ask_gemma(messages):
    try:
        outputs = nlp.model(messages, max_new_tokens=256)
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
        return assistant_response
        
    except Exception as e:
        print(e)
        