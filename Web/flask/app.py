from forensix.shared import *
from flask_cors import CORS
from forensix import auth, internal

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")
CORS(app)

app.register_blueprint(auth.auth)
app.register_blueprint(internal.internal)

@app.route('/')
def main():
    return make_response("Hello", 200)

@app.errorhandler(404)
def page_not_found():
    return make_response("The requested URL does not exist", 404)

@app.route("/query", methods=["POST"])
def query():
    data = json.loads(request.data) 
    query = data["query"]
    
    return make_response(query, 200)

    