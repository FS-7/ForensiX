from flask import Flask, request, session, make_response
from flask_cors import  CORS

import face_recognition as f_r

app = Flask(__name__)
#app.secret_key = os.getenv("SESSION_KEY")
cors = CORS(app)

fr = None

class FR:
    def __init__(self):
        self.model = None
        
    def isLoaded(self):
        return False if self.model == None else True
        
fr = FR()

@app.route('/')
def main():
    return make_response("Server running...", 200)

@app.route('/checkStatus', methods=["GET"])
def checkStatus():
    return make_response(f"Face recognition model ready?: {str(fr.isLoaded() != None)}", 200)

@app.route("/fr", methods=[])
def face_recognition():
    return 