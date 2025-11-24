from forensix.shared import *
from forensix import auth, internal, cases

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app)

app.register_blueprint(auth.auth)
app.register_blueprint(internal.internal)
app.register_blueprint(cases.cases)

@app.route('/')
def main():
    return make_response("Hello", 200)

if __name__ == "__main__":    
    pass

init_db()