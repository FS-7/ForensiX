from forensix.shared import *
from forensix import threat, parser

internal = Blueprint('internal', __name__, url_prefix='/internal')
internal.register_blueprint(threat.threat)
internal.register_blueprint(parser.parser)

@internal.route('/', methods=["Get"])
def internal_index():
    return make_response("", 200)

@internal.route('/preprocess')
def preprocessing():
    Normalize()
    GenerateEmbeddings()
    return

@internal.route('/classify')
def classify():
    return 

@internal.route('/llm_safety')
def llm_safety():
    return 

def Normalize():
    return

def GenerateEmbeddings():
    return