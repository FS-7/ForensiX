from forensix.shared import *

threat = Blueprint('threat', __name__, url_prefix='/threat')

@threat.route('/', methods=["Get"])
def internal():
    return make_response("", 200)

@threat.route('/analyze')
def analyze():
    return

@threat.route('/batch')
def batch():
    return

@threat.route('/report')
def report():
    return

def load_model():
    return