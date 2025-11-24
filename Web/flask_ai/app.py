from ai.shared import *
#from ai import 

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
#cors = CORS(app)

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    print(asr_model != None, nlp_model != None, zsc_model != None)
    
@app.route('/asr')
def asr():
    pass

@app.route('/nlp')
def nlp():
    pass

@app.route('/zsc')
def zsc():
    pass

def init():
    try:
        load_ASR()
        load_NLP()
        load_ZSC()
    except Exception as e:
        print(e)