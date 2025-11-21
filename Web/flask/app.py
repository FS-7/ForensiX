from forensix.shared import *
from flask_cors import CORS
from forensix import auth, internal, cases

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)

app.register_blueprint(auth.auth)
app.register_blueprint(internal.internal)
app.register_blueprint(cases.cases)

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

if __name__ == "__main__":    
    pass

init_db()