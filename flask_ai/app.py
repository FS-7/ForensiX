from ai.shared import *

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

@app.route('/')
def main():
    return make_response("", 200)

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(str(asr != None and nlp != None), 200)
    
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

@app.route('/nlp', methods=["POST"])
def ask_gemma():
    try:
        data = request.form
        query = data["messages"]
        messages = [
            {
                "role": "user", 
                "content": query
            }
        ]
        print(messages)
        outputs = nlp.model(messages, max_new_tokens=128)
        
        print(outputs)
        assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
        return make_response(assistant_response, 200)
        
    except Exception as e:
        print(e)
        return make_response("", 400)