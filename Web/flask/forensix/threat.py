from forensix.shared import *
from forensix.parser import parseSMS_CSV, parseLogsCSV, parseContactsCSV, parseSMS_SQL, parseLogsSQL

threat = Blueprint('threat', __name__, url_prefix='/threat')

@threat.route('/', methods=["GET"])
def threat_index():
    return make_response("", 200)

@threat.route('/analyze')
def analyze():
    classifier = pipeline("zero-shot-classification", "MoritzLaurer/deberta-v3-large-zeroshot-v2.0")

    loc = os.getenv('DATA')
    
    sms_documents = parseSMS_CSV(loc)

    candidate_labels = [
        "identity_attack",
        "sexual_explicit",
        "threat",
        "toxicity",
        "normal",
        "extremism"
    ]

    res = defaultdict(str)
    keys = set([x.metadata["Sender"] for x in reversed(sms_documents)])

    for k in keys:
        for i in sms_documents:
            if k == i.metadata["Sender"]:
                res[k] = res[k] + i.page_content + ". "

    for k in res.keys():
        print(k, classifier(res[k], candidate_labels))
    return

@threat.route('/batch')
def batch():
    return

@threat.route('/report')
def report():
    return

def load_model():
    return