from forensix.shared import *
from forensix import auth, internal, cases

app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cors = CORS(app)

app.register_blueprint(auth.auth)
app.register_blueprint(internal.internal)
app.register_blueprint(cases.cases)

@app.route('/')
def main():
    print("Request to /")
    return make_response("Hello", 200)

if __name__ == "__main__":    
    pass

init_db()